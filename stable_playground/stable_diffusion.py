"""Test drive my container env with stable diffusion."""

import random
import sys

from diffusers import StableDiffusionPipeline
from torch.cuda.amp import autocast


# Could probably use an inline lambda for this
def dummy(images, **kwargs):
    return images, False


# Read prompt from command line
args = sys.argv
del args[0]
prompt = " ".join(args)

pipe = StableDiffusionPipeline.from_pretrained(
    "/models/stablediff", local_files_only=True
)
pipe.to("cuda")  # Run on GPU
pipe.safety_checker = dummy  # Disable NSFW check

# Run until we exit with CTRL+C
while True:
    with autocast():
        n = random.randint(1000, 9999)
        image = pipe(prompt, guidance_scale=7.5)["images"][0]
        image.save(f"diffusions/{prompt}-{n}.jpeg")
