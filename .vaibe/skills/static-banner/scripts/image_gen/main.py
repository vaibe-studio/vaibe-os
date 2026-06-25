"""CLI entry point for image generation via ComfyUI."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from character_parser import (
    NEGATIVE_PROMPT,
    STYLE_BLOCK,
    build_prompt,
    find_character,
    get_reference_image_path,
    list_characters,
)
from comfyui_client import ComfyUIClient
from workflow_builder import build_txt2img_workflow, build_ipadapter_workflow


def cmd_status(args):
    """Check if ComfyUI is running."""
    client = ComfyUIClient(host=args.host, port=args.port)
    if client.is_running():
        print(f"ComfyUI is running at {client.base_url}")
    else:
        print(f"ComfyUI is NOT running at {client.base_url}")
        print("Start it with: run_amd_gpu.bat (or python main.py --directml)")
        sys.exit(1)


def cmd_list_characters(args):
    """List all available characters."""
    chars = list_characters()
    print(f"Available characters ({len(chars)}):\n")
    for c in chars:
        print(f"  {c.name_ru} ({c.name_en}) — {c.role}")
        has_refs = "yes" if c.ref_front else "no"
        print(f"    Reference images: {has_refs}")
        print()


def cmd_generate(args):
    """Generate an image."""
    client = ComfyUIClient(host=args.host, port=args.port)
    if not client.is_running():
        print(f"Error: ComfyUI is not running at {client.base_url}")
        sys.exit(1)

    if args.character:
        char = find_character(args.character)
        if not char:
            print(f"Error: character '{args.character}' not found")
            print("Available characters:")
            for c in list_characters():
                print(f"  - {c.name_ru}")
            sys.exit(1)

        prompt = build_prompt(char, args.scene or "neutral pose, simple background")
        print(f"Character: {char.name_ru}")
        print(f"Prompt:\n{prompt}\n")

        ref_path = get_reference_image_path(
            char, view="front", workspace_root=Path(args.workspace)
        )
        use_ipadapter = args.ipadapter and ref_path and ref_path.exists()

        if use_ipadapter:
            print(f"Using IP-Adapter with reference: {ref_path}")
            workflow = build_ipadapter_workflow(
                positive_prompt=prompt,
                negative_prompt=NEGATIVE_PROMPT,
                reference_image_path=str(ref_path),
                checkpoint=args.checkpoint,
                width=args.width,
                height=args.height,
                steps=args.steps,
                cfg=args.cfg,
                seed=args.seed,
            )
        else:
            if args.ipadapter and ref_path and not ref_path.exists():
                print(f"Warning: reference image not found at {ref_path}, falling back to txt2img")
            workflow = build_txt2img_workflow(
                positive_prompt=prompt,
                negative_prompt=NEGATIVE_PROMPT,
                checkpoint=args.checkpoint,
                width=args.width,
                height=args.height,
                steps=args.steps,
                cfg=args.cfg,
                seed=args.seed,
            )
    elif args.prompt:
        prompt = args.prompt
        workflow = build_txt2img_workflow(
            positive_prompt=prompt,
            negative_prompt=NEGATIVE_PROMPT,
            checkpoint=args.checkpoint,
            width=args.width,
            height=args.height,
            steps=args.steps,
            cfg=args.cfg,
            seed=args.seed,
        )
    else:
        print("Error: provide --character or --prompt")
        sys.exit(1)

    output_path = Path(args.output)
    saved = client.generate_and_save(workflow, output_path, timeout=args.timeout)
    print(f"\nGeneration complete. Files saved: {len(saved)}")
    for f in saved:
        print(f"  {f}")


def main():
    parser = argparse.ArgumentParser(
        prog="uv run --project .vaibe/skills/static-banner/scripts/image_gen .vaibe/skills/static-banner/scripts/image_gen/main.py",
        description="Generate images via ComfyUI API using vAIbe-media character sheets",
    )
    parser.add_argument("--host", default="127.0.0.1", help="ComfyUI host")
    parser.add_argument("--port", type=int, default=8188, help="ComfyUI port")
    parser.add_argument("--workspace", default=".", help="Path to vAIbe-OS workspace root")

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("status", help="Check if ComfyUI is running")
    subparsers.add_parser("list-characters", help="List available characters")

    gen = subparsers.add_parser("generate", help="Generate an image")
    gen.add_argument("--character", "-c", help="Character name (Russian or English)")
    gen.add_argument("--scene", "-s", help="Scene description for the character")
    gen.add_argument("--prompt", "-p", help="Custom prompt (instead of character)")
    gen.add_argument("--output", "-o", default="output.png", help="Output file path")
    gen.add_argument("--ipadapter", action="store_true", help="Use IP-Adapter with reference image")
    gen.add_argument("--checkpoint", default="sd_xl_base_1.0.safetensors", help="Model checkpoint")
    gen.add_argument("--width", type=int, default=1024, help="Image width")
    gen.add_argument("--height", type=int, default=1024, help="Image height")
    gen.add_argument("--steps", type=int, default=25, help="Sampling steps")
    gen.add_argument("--cfg", type=float, default=7.0, help="CFG scale")
    gen.add_argument("--seed", type=int, default=-1, help="Seed (-1 for random)")
    gen.add_argument("--timeout", type=int, default=600, help="Max wait time in seconds")

    args = parser.parse_args()

    if args.command == "status":
        cmd_status(args)
    elif args.command == "list-characters":
        cmd_list_characters(args)
    elif args.command == "generate":
        cmd_generate(args)


if __name__ == "__main__":
    main()
