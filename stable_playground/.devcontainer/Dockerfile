FROM mcr.microsoft.com/devcontainers/python:0-3.11
RUN python -m pip install --upgrade pip && \
	pip install accelerate diffusers transformers torch
COPY save_hf_model.py /save_hf_model.py
RUN python /save_hf_model.py