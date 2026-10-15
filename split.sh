#!/usr/bin/env bash

video="${1}"
outdir="${video%.*}"

mkdir -p "$outdir"

ffmpeg -i "$video" \
  -fps_mode passthrough \
  -start_number 0 \
  -q:v 2 \
  "$outdir/frame_%06d.jpg"