#!/bin/bash
# Generate videos in batch from metadata JSON
# Usage: bash scripts/infer_batch.sh --metadata_path data/example/metadata.json

CHECKPOINT_DIR="${CHECKPOINT_DIR:-./models/train/wan_lora_14B}"
METADATA_PATH="${METADATA_PATH:-data/example/metadata.json}"
OUTPUT_DIR="${OUTPUT_DIR:-./outputs}"
MODEL_NAME="${MODEL_NAME:-Wan-AI/Wan2.1-T2V-14B}"
IS_LORA="${IS_LORA:-true}"
HEIGHT="${HEIGHT:-480}"
WIDTH="${WIDTH:-832}"
NUM_FRAMES="${NUM_FRAMES:-16}"
INFERENCE_STEPS="${INFERENCE_STEPS:-50}"
GUIDANCE_SCALE="${GUIDANCE_SCALE:-7.5}"

LORA_FLAG=""
if [ "$IS_LORA" = "true" ]; then
  LORA_FLAG="--is_lora"
fi

python inference.py \
  --model_name "$MODEL_NAME" \
  --checkpoint_dir "$CHECKPOINT_DIR" \
  --metadata_path "$METADATA_PATH" \
  --output_dir "$OUTPUT_DIR" \
  --height "$HEIGHT" \
  --width "$WIDTH" \
  --num_frames "$NUM_FRAMES" \
  --num_inference_steps "$INFERENCE_STEPS" \
  --guidance_scale "$GUIDANCE_SCALE" \
  $LORA_FLAG
