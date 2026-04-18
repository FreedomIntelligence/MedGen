#!/bin/bash
# Generate videos using LoRA-fine-tuned 1.3B model
# Usage: bash scripts/infer_lora_1.3B.sh --prompt "your prompt here"

CHECKPOINT_DIR="${CHECKPOINT_DIR:-./models/train/wan_lora_1.3B}"
OUTPUT_DIR="${OUTPUT_DIR:-./outputs}"
HEIGHT="${HEIGHT:-480}"
WIDTH="${WIDTH:-832}"
NUM_FRAMES="${NUM_FRAMES:-16}"
INFERENCE_STEPS="${INFERENCE_STEPS:-50}"
GUIDANCE_SCALE="${GUIDANCE_SCALE:-7.5}"

python inference.py \
  --model_name "Wan-AI/Wan2.1-T2V-1.3B" \
  --checkpoint_dir "$CHECKPOINT_DIR" \
  --is_lora \
  --output_dir "$OUTPUT_DIR" \
  --height "$HEIGHT" \
  --width "$WIDTH" \
  --num_frames "$NUM_FRAMES" \
  --num_inference_steps "$INFERENCE_STEPS" \
  --guidance_scale "$GUIDANCE_SCALE" \
  "$@"
