"""Build ComfyUI workflow dicts programmatically.

These workflows are designed for SDXL + DirectML on AMD GPU (8 GB VRAM).
"""

import random
from typing import Optional


def build_txt2img_workflow(
    positive_prompt: str,
    negative_prompt: str,
    checkpoint: str = "sd_xl_base_1.0.safetensors",
    width: int = 1024,
    height: int = 1024,
    steps: int = 25,
    cfg: float = 7.0,
    seed: int = -1,
    sampler: str = "euler_ancestral",
    scheduler: str = "normal",
    output_prefix: str = "vaibe-media",
) -> dict:
    """Build a basic txt2img workflow for ComfyUI API."""
    if seed < 0:
        seed = random.randint(0, 2**32 - 1)

    return {
        "3": {
            "class_type": "KSampler",
            "inputs": {
                "model": ["4", 0],
                "positive": ["6", 0],
                "negative": ["7", 0],
                "latent_image": ["5", 0],
                "seed": seed,
                "steps": steps,
                "cfg": cfg,
                "sampler_name": sampler,
                "scheduler": scheduler,
                "denoise": 1.0,
            },
        },
        "4": {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {
                "ckpt_name": checkpoint,
            },
        },
        "5": {
            "class_type": "EmptyLatentImage",
            "inputs": {
                "width": width,
                "height": height,
                "batch_size": 1,
            },
        },
        "6": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "text": positive_prompt,
                "clip": ["4", 1],
            },
        },
        "7": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "text": negative_prompt,
                "clip": ["4", 1],
            },
        },
        "8": {
            "class_type": "VAEDecode",
            "inputs": {
                "samples": ["3", 0],
                "vae": ["4", 2],
            },
        },
        "9": {
            "class_type": "SaveImage",
            "inputs": {
                "images": ["8", 0],
                "filename_prefix": output_prefix,
            },
        },
    }


def build_ipadapter_workflow(
    positive_prompt: str,
    negative_prompt: str,
    reference_image_path: str,
    checkpoint: str = "sd_xl_base_1.0.safetensors",
    ipadapter_model: str = "ip-adapter-plus_sdxl_vit-h.safetensors",
    clip_vision_model: str = "CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors",
    width: int = 1024,
    height: int = 1024,
    steps: int = 30,
    cfg: float = 7.0,
    seed: int = -1,
    ipadapter_weight: float = 0.8,
    sampler: str = "euler_ancestral",
    scheduler: str = "normal",
    output_prefix: str = "vaibe-media-ipadapter",
) -> dict:
    """Build an IP-Adapter workflow for character-consistent generation.

    Requires ComfyUI_IPAdapter_plus custom nodes installed.
    """
    if seed < 0:
        seed = random.randint(0, 2**32 - 1)

    return {
        "4": {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {
                "ckpt_name": checkpoint,
            },
        },
        "10": {
            "class_type": "IPAdapterModelLoader",
            "inputs": {
                "ipadapter_file": ipadapter_model,
            },
        },
        "11": {
            "class_type": "CLIPVisionLoader",
            "inputs": {
                "clip_name": clip_vision_model,
            },
        },
        "12": {
            "class_type": "LoadImage",
            "inputs": {
                "image": reference_image_path,
            },
        },
        "13": {
            "class_type": "IPAdapterAdvanced",
            "inputs": {
                "model": ["4", 0],
                "ipadapter": ["10", 0],
                "clip_vision": ["11", 0],
                "image": ["12", 0],
                "weight": ipadapter_weight,
                "weight_type": "style+composition",
                "combine_embeds": "concat",
                "start_at": 0.0,
                "end_at": 1.0,
                "embeds_scaling": "V only",
            },
        },
        "5": {
            "class_type": "EmptyLatentImage",
            "inputs": {
                "width": width,
                "height": height,
                "batch_size": 1,
            },
        },
        "6": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "text": positive_prompt,
                "clip": ["4", 1],
            },
        },
        "7": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "text": negative_prompt,
                "clip": ["4", 1],
            },
        },
        "3": {
            "class_type": "KSampler",
            "inputs": {
                "model": ["13", 0],
                "positive": ["6", 0],
                "negative": ["7", 0],
                "latent_image": ["5", 0],
                "seed": seed,
                "steps": steps,
                "cfg": cfg,
                "sampler_name": sampler,
                "scheduler": scheduler,
                "denoise": 1.0,
            },
        },
        "8": {
            "class_type": "VAEDecode",
            "inputs": {
                "samples": ["3", 0],
                "vae": ["4", 2],
            },
        },
        "9": {
            "class_type": "SaveImage",
            "inputs": {
                "images": ["8", 0],
                "filename_prefix": output_prefix,
            },
        },
    }
