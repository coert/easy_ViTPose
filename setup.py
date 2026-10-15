from setuptools import find_packages, setup

setup(
    name="easy_ViTPose",
    author="JunkyByte",
    author_email="adriano.donninelli@hotmail.it",
    version="1.1",
    url="https://github.com/JunkyByte/easy_ViTPose",
    packages=find_packages(include=["easy_ViTPose", "easy_ViTPose.*"]),
)
