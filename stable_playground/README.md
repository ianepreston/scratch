# stable_playground
Mess around with stable diffusion

This is definitely for experimentation.

I want to be able to run gpu accelerated workloads within a dev container, and I want a way for pretrained models to persist in the container so I don't have to download them every time. This meets both needs.

The actual code is hacked together. Sources:
https://constant.meiring.nz/playing/2022/08/04/playing-with-stable-diffusion.html
https://ismailaslan1.medium.com/how-to-containerize-a-huggingface-transformers-model-using-docker-and-flask-a8df93ea2dc3

# Getting this working on your machine

No promises. Make sure you have docker, cuda, and the nvidia container runtime all set up. I'd like to how to do that but it seems to change
all the time so good luck with google? 

¯\\_(ツ)_/¯

Other than that change the source for where the diffusions will be saved to a location you actually have in `devcontainer.json` and
add `.env` file in the `.devcontainer` folder with your API token for huggingface (you can get one for free) in the form `HUGGINGFACE_KEY=<your key here>`
