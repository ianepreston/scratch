import os

import torch
from diffusers import StableDiffusionPipeline

model_path = "/models/stablediff"
pipe = StableDiffusionPipeline.from_pretrained(
    "CompVis/stable-diffusion-v1-4",
    revision="fp16",
    torch_dtype=torch.float16,
    use_auth_token=os.getenv("HUGGINGFACE_KEY"),
)
pipe.save_pretrained(model_path)
