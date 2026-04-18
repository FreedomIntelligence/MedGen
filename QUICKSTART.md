# Quick Start Guide

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

## 2. Prepare Your Dataset

Create a JSON metadata file with video paths and prompts:

```bash
mkdir -p data/videos
# Place your videos in data/videos/
# Create data/metadata.json with the format shown in data/example/metadata.json
```

## 3. Train a Model

### LoRA Training (Recommended for Quick Start)

```bash
# Single GPU - 1.3B model
bash scripts/train_lora_1.3B.sh

# Dual GPU - 14B model
bash scripts/train_lora_14B.sh
```

Set custom paths:
```bash
export DATASET_BASE_PATH="/path/to/videos"
export DATASET_METADATA="data/metadata.json"
bash scripts/train_lora_1.3B.sh
```

### Full Parameter Training

```bash
# Single GPU - 1.3B model
bash scripts/train_full_1.3B.sh

# Dual GPU with DeepSpeed - 14B model
bash scripts/train_full_14B.sh
```

## 4. Generate Videos

### Single Video Generation

```bash
# Using LoRA checkpoint
python inference.py \
  --model_name "Wan-AI/Wan2.1-T2V-1.3B" \
  --checkpoint_dir "./models/train/wan_lora_1.3B" \
  --is_lora \
  --prompt "A doctor performing surgery" \
  --output_path "output.mp4"
```

### Batch Generation

```bash
bash scripts/infer_batch.sh \
  --metadata_path data/metadata.json \
  --output_dir outputs
```

## Environment Variables

```bash
# Training
export DATASET_BASE_PATH="/path/to/videos"
export DATASET_METADATA="data/metadata.json"
export OUTPUT_PATH="./models/checkpoints"
export NUM_EPOCHS=2
export LEARNING_RATE=1e-4
export BATCH_SIZE=1
export GRADIENT_ACCUMULATION=4

# Inference
export CHECKPOINT_DIR="./models/train/wan_lora_1.3B"
export OUTPUT_DIR="./outputs"
export INFERENCE_STEPS=50
export GUIDANCE_SCALE=7.5
```

## Troubleshooting

**Out of Memory (OOM):**
- Reduce `BATCH_SIZE` or `GRADIENT_ACCUMULATION`
- Use LoRA instead of full training
- Enable gradient checkpointing (default: on)

**CUDA Errors:**
- Ensure PyTorch is installed with correct CUDA version
- Check GPU availability: `python -c "import torch; print(torch.cuda.is_available())"`

**Model Download Issues:**
- Models are downloaded from Hugging Face Hub
- Ensure internet connection and sufficient disk space (~50GB for 14B model)

