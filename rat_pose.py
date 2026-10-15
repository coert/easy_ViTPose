import cv2
import numpy as np
import torch

from easy_ViTPose import VitInference
from easy_ViTPose.configs.ViTPose_ap10k import model_base
from easy_ViTPose.vit_models.model import ViTPose
from easy_ViTPose.vit_utils.inference import pad_image

device = (
    "cuda"
    if torch.cuda.is_available()
    else "mps"
    if torch.backends.mps.is_available()
    else "cpu"
)
print(f"Using {device}")

model = ViTPose(model_base)
checkpoint = torch.load(
    "models/vitpose-b-ap10k.pth",
    map_location="cpu",
    weights_only=True,
)
model.load_state_dict(checkpoint.get("state_dict", checkpoint))
model = model.to(device).eval()

image = cv2.imread(
    "data/Translational neuroimaging group - rodents/AI PR Analysis/mp4/Basler_acA720-520uc__40502463__20250312_095111453_Failure Pellet to Box 2+ reaches/frame_000500.jpg"
)
if image is None:
    raise FileNotFoundError("Cannot read input image")

rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
padded, (left, top) = pad_image(rgb, 3 / 4)
height, width = padded.shape[:2]

# Match the wrapper's RGB preprocessing.
inputs = cv2.resize(padded, (192, 256)) / 255.0
inputs = (inputs - np.array([0.485, 0.456, 0.406])) / np.array([0.229, 0.224, 0.225])
inputs = inputs.transpose(2, 0, 1)[None].astype(np.float32)

with torch.inference_mode():
    heatmaps = model(torch.from_numpy(inputs).to(device))
    heatmaps = heatmaps.cpu().numpy()

# The wrapper returns (y, x, score).
points = VitInference.postprocess(heatmaps, width, height)[0]
points[:, 0] -= top
points[:, 1] -= left

names = [
    "left_eye",
    "right_eye",
    "nose",
    "neck",
    "tail_base",
    "left_shoulder",
    "left_elbow",
    "left_front_paw",
    "right_shoulder",
    "right_elbow",
    "right_front_paw",
    "left_hip",
    "left_knee",
    "left_back_paw",
    "right_hip",
    "right_knee",
    "right_back_paw",
]

with open("data/rat_keypoints.csv", "w") as output:
    output.write("keypoint,x,y,score\n")
    for name, (y, x, score) in zip(names, points):
        output.write(f"{name},{x:.2f},{y:.2f},{score:.4f}\n")
        if score >= 0.3:
            position = (round(float(x)), round(float(y)))
            cv2.circle(image, position, 3, (0, 255, 0), -1)
            cv2.putText(
                image,
                name,
                position,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.35,
                (0, 255, 0),
                1,
            )

cv2.imwrite("data/rat_pose.jpg", image)
print("Saved data/rat_pose.jpg and data/rat_keypoints.csv")
