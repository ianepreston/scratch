#!/bin/bash

echo "Starting the build"
docker build -t ytdlp:latest .
docker run --mount type=bind,source=/mnt/z/Misc\ Videos/ytdlptest,target=/data ytdlp