#!/bin/bash
# LoRA fine-tuning for Wan2.1-T2V-1.3B model
# Usage: bash scripts/train_lora_1.3B.sh

set -e

# Configuration
DATASET_BASE_PATH="${DATASET_BASE_PATH:-.}"
DATASET_METADATA="${DATASET_METADATA:-data/example/metadata.json}"
OUTPUT_PATH="${OUTPUT_PATH:-./models/train/wan_lora_1.3B}"
NUM_EPOCHS="${NUM_EPOCHS:-2}"
LEARNING_RATE="${LEARNING_RATE:-1e-4}"
BATCH_SIZE="${BATCH_SIZE:-1}"
GRADIENT_ACCUMULATION="${GRADIENT_ACCUMULATION:-4}"

echo "=== Wan2.1-T2V-1.3B LoRA Fine-tuning ==="
echo "Dataset: $DATASET_BASE_PATH"
echo "Metadata: $DATASET_METADATA"
echo "Output: $OUTPUT_PATH"
echo "Start time: $(date)"

accelerate launch --config_file configs/accelerate_1gpu.yaml \
  train.py \
  --dataset_base_path "$DATASET_BASE_PATH" \
  --dataset_metadata_path "$DATASET_METADATA" \
  --height 480 --width 832 \
  --num_frames 16 \
  --model_id_with_origin_paths "Wan-AI/Wan2.1-T2V-1.3B:diffusion_pytorch_model*.safetensors,Wan-AI/Wan2.1-T2V-1.3B:models_t5_umt5-xxl-enc-bf16.pth,Wan-AI/Wan2.1-T2V-1.3B:Wan2.1_VAE.pth" \
  --learning_rate "$LEARNING_RATE" \
  --num_epochs "$NUM_EPOCHS" \
  --per_gpu_batch_size "$BATCH_SIZE" \
  --gradient_accumulation_steps "$GRADIENT_ACCUMULATION" \
  --output_path "$OUTPUT_PATH" \
  --lora_base_model "dit" \
  --lora_rank 32 \
  --save_steps 500

echo "=== Training Complete ==="
echo "End time: $(date)"
ls -lh "$OUTPUT_PATH"/
