# Project Structure

```
./
├── train.py                          # Main training script
├── inference.py                      # Video generation script
├── README.md                         # Comprehensive documentation
├── QUICKSTART.md                     # Quick start guide
├── requirements.txt                  # Python dependencies
├── .gitignore                        # Git ignore rules
│
├── scripts/                          # Training and inference scripts
│   ├── train_lora_1.3B.sh           # LoRA training for 1.3B model
│   ├── train_lora_14B.sh            # LoRA training for 14B model
│   ├── train_full_1.3B.sh           # Full training for 1.3B model
│   ├── train_full_14B.sh            # Full training for 14B model (DeepSpeed)
│   ├── infer_lora_1.3B.sh           # Inference with 1.3B LoRA checkpoint
│   ├── infer_lora_14B.sh            # Inference with 14B LoRA checkpoint
│   ├── infer_full_1.3B.sh           # Inference with 1.3B full checkpoint
│   ├── infer_full_14B.sh            # Inference with 14B full checkpoint
│   └── infer_batch.sh               # Batch inference from metadata JSON
│
├── configs/                          # Accelerate configuration files
│   ├── accelerate_1gpu.yaml         # Single GPU configuration
│   ├── accelerate_2gpu.yaml         # Dual GPU configuration
│   └── accelerate_deepspeed_2gpu.yaml # DeepSpeed ZeRO-2 configuration
│
└── data/                             # Dataset directory
    └── example/
        └── metadata.json            # Example metadata format
```

## File Descriptions

### Core Scripts

- **train.py**: Main training entry point using DiffSynth framework
  - Supports both LoRA and full-parameter training
  - Handles video loading, preprocessing, and loss computation
  - Compatible with Accelerate and DeepSpeed

- **inference.py**: Video generation from trained models
  - Loads base Wan2.1 pipeline
  - Supports LoRA adapter loading
  - Single and batch video generation
  - Configurable inference parameters

### Training Scripts

All training scripts are configurable via environment variables:

- `DATASET_BASE_PATH`: Path to video directory
- `DATASET_METADATA`: Path to metadata JSON
- `OUTPUT_PATH`: Checkpoint output directory
- `NUM_EPOCHS`: Number of training epochs
- `LEARNING_RATE`: Learning rate
- `BATCH_SIZE`: Batch size per GPU
- `GRADIENT_ACCUMULATION`: Gradient accumulation steps

### Inference Scripts

All inference scripts support:

- `CHECKPOINT_DIR`: Directory containing checkpoints
- `OUTPUT_DIR`: Output directory for generated videos
- `HEIGHT`, `WIDTH`: Video resolution
- `NUM_FRAMES`: Number of frames
- `INFERENCE_STEPS`: Number of diffusion steps
- `GUIDANCE_SCALE`: Classifier-free guidance scale

### Accelerate Configs

- **accelerate_1gpu.yaml**: Single GPU with bfloat16 mixed precision
- **accelerate_2gpu.yaml**: Dual GPU with distributed data parallel
- **accelerate_deepspeed_2gpu.yaml**: Dual GPU with DeepSpeed ZeRO-2 and CPU offloading

### Data Format

Metadata JSON format:
```json
[
  {
    "id": "unique_video_id",
    "video": "relative/path/to/video.mp4",
    "prompt": "Text description of video content"
  }
]
```

## Training Modes

### LoRA Fine-tuning
- Memory efficient (50% less VRAM)
- Faster training
- Good for domain adaptation
- Requires adapter loading during inference

### Full Parameter Training
- Full model fine-tuning
- Better for significant domain shifts
- Higher memory requirements
- Direct inference without adapters

## GPU Requirements

| Mode | Model | VRAM | Setup |
|------|-------|------|-------|
| LoRA | 1.3B | ~20GB | 1x GPU |
| LoRA | 14B | ~40GB | 2x GPU |
| Full | 1.3B | ~40GB | 1x GPU |
| Full | 14B | ~80GB | 2x GPU + DeepSpeed |

## Checkpoint Management

Checkpoints are saved at regular intervals:
- LoRA: Every 500 steps
- Full: Every 500-1000 steps

Latest checkpoint is automatically detected and used for:
- Training resumption
- Inference

Checkpoint directory structure:
```
models/train/wan_lora_1.3B/
├── step-500/
├── step-1000/
├── step-1500/
└── ...
```

## Dependencies

Core dependencies (see requirements.txt):
- torch >= 2.0.0
- accelerate >= 0.24.0
- deepspeed >= 0.12.0
- diffsynth-studio >= 0.1.0
- peft >= 0.4.0
- transformers >= 4.30.0

## Quick Commands

```bash
# Install
pip install -r requirements.txt

# Train LoRA on 1.3B
bash scripts/train_lora_1.3B.sh

# Train full on 14B with DeepSpeed
bash scripts/train_full_14B.sh

# Generate single video
python inference.py --model_name "Wan-AI/Wan2.1-T2V-1.3B" \
  --checkpoint_dir "./models/train/wan_lora_1.3B" \
  --is_lora --prompt "your prompt"

# Batch generation
bash scripts/infer_batch.sh --metadata_path data/metadata.json
```
