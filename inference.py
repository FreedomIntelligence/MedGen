import os
import json
import torch
import argparse
from pathlib import Path
from diffsynth import DiffSynthPipeline
from diffsynth.models import WanVideoModel
from peft import PeftModel


def load_pipeline(model_name, device="cuda"):
    """Load the base Wan2.1 pipeline."""
    pipeline = DiffSynthPipeline.from_pretrained(model_name)
    pipeline = pipeline.to(device)
    return pipeline


def load_lora_checkpoint(pipeline, checkpoint_path):
    """Load LoRA adapter from checkpoint."""
    model = pipeline.dit
    model = PeftModel.from_pretrained(model, checkpoint_path)
    pipeline.dit = model
    return pipeline


def load_full_checkpoint(checkpoint_path, model_name, device="cuda"):
    """Load full model checkpoint."""
    pipeline = DiffSynthPipeline.from_pretrained(model_name)

    # Load checkpoint state dict
    state_dict = torch.load(checkpoint_path, map_location=device)
    pipeline.dit.load_state_dict(state_dict)
    pipeline = pipeline.to(device)
    return pipeline


def find_latest_checkpoint(checkpoint_dir):
    """Find the latest checkpoint in a directory."""
    checkpoint_dir = Path(checkpoint_dir)
    if not checkpoint_dir.exists():
        return None

    checkpoints = sorted(checkpoint_dir.glob("step-*"))
    if checkpoints:
        return str(checkpoints[-1])
    return None


def generate_single(
    pipeline,
    prompt,
    height=480,
    width=832,
    num_frames=16,
    num_inference_steps=50,
    guidance_scale=7.5,
    output_path="output.mp4"
):
    """Generate a single video from a text prompt."""
    with torch.no_grad():
        video = pipeline(
            prompt=prompt,
            height=height,
            width=width,
            num_frames=num_frames,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
        )

    # Save video
    video.save(output_path)
    print(f"Video saved to {output_path}")
    return video


def generate_batch(
    pipeline,
    metadata_path,
    output_dir="outputs",
    height=480,
    width=832,
    num_frames=16,
    num_inference_steps=50,
    guidance_scale=7.5,
):
    """Generate videos from a metadata JSON file."""
    os.makedirs(output_dir, exist_ok=True)

    with open(metadata_path, 'r') as f:
        metadata = json.load(f)

    for item in metadata:
        video_id = item.get('id', 'unknown')
        prompt = item.get('prompt', '')

        output_path = os.path.join(output_dir, f"{video_id}.mp4")

        print(f"Generating {video_id}: {prompt}")
        generate_single(
            pipeline,
            prompt,
            height=height,
            width=width,
            num_frames=num_frames,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            output_path=output_path
        )


def main():
    parser = argparse.ArgumentParser(description="Generate videos using Wan2.1 model")
    parser.add_argument("--model_name", type=str, default="Wan-AI/Wan2.1-T2V-14B",
                        help="Base model name")
    parser.add_argument("--checkpoint_path", type=str, default=None,
                        help="Path to checkpoint (LoRA or full)")
    parser.add_argument("--checkpoint_dir", type=str, default=None,
                        help="Directory to search for latest checkpoint")
    parser.add_argument("--is_lora", action="store_true",
                        help="Whether checkpoint is LoRA adapter")
    parser.add_argument("--prompt", type=str, default=None,
                        help="Text prompt for single video generation")
    parser.add_argument("--metadata_path", type=str, default=None,
                        help="Path to metadata JSON for batch generation")
    parser.add_argument("--output_path", type=str, default="output.mp4",
                        help="Output path for single video")
    parser.add_argument("--output_dir", type=str, default="outputs",
                        help="Output directory for batch generation")
    parser.add_argument("--height", type=int, default=480,
                        help="Video height")
    parser.add_argument("--width", type=int, default=832,
                        help="Video width")
    parser.add_argument("--num_frames", type=int, default=16,
                        help="Number of frames")
    parser.add_argument("--num_inference_steps", type=int, default=50,
                        help="Number of inference steps")
    parser.add_argument("--guidance_scale", type=float, default=7.5,
                        help="Guidance scale")
    parser.add_argument("--device", type=str, default="cuda",
                        help="Device to use")

    args = parser.parse_args()

    # Load pipeline
    print(f"Loading model: {args.model_name}")
    pipeline = load_pipeline(args.model_name, device=args.device)

    # Load checkpoint if provided
    if args.checkpoint_dir:
        checkpoint_path = find_latest_checkpoint(args.checkpoint_dir)
        if checkpoint_path:
            print(f"Found checkpoint: {checkpoint_path}")
            args.checkpoint_path = checkpoint_path

    if args.checkpoint_path:
        print(f"Loading checkpoint: {args.checkpoint_path}")
        if args.is_lora:
            pipeline = load_lora_checkpoint(pipeline, args.checkpoint_path)
        else:
            pipeline = load_full_checkpoint(args.checkpoint_path, args.model_name, args.device)

    # Generate videos
    if args.prompt:
        print(f"Generating video: {args.prompt}")
        generate_single(
            pipeline,
            args.prompt,
            height=args.height,
            width=args.width,
            num_frames=args.num_frames,
            num_inference_steps=args.num_inference_steps,
            guidance_scale=args.guidance_scale,
            output_path=args.output_path
        )
    elif args.metadata_path:
        print(f"Generating batch from: {args.metadata_path}")
        generate_batch(
            pipeline,
            args.metadata_path,
            output_dir=args.output_dir,
            height=args.height,
            width=args.width,
            num_frames=args.num_frames,
            num_inference_steps=args.num_inference_steps,
            guidance_scale=args.guidance_scale,
        )
    else:
        print("Please provide either --prompt or --metadata_path")


if __name__ == "__main__":
    main()
