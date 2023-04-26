FROM ubuntu:22.10

# Install updates and dependencies
RUN apt update && \
	DEBIAN_FRONTEND=noninteractive apt install -y software-properties-common && \	
	add-apt-repository ppa:tomtomtom/yt-dlp && \
	apt update && \
	apt upgrade -y && \
	DEBIAN_FRONTEND=noninteractive apt install -y yt-dlp && \
	rm -rf /var/lib/apt/lists/* && \
	apt clean

WORKDIR /config
COPY entrypoint.sh entrypoint.sh
COPY format.txt format.txt
COPY ytdlconf ytdlconf
COPY downloads downloads
COPY ytdlp.py ytdlp.py
CMD [ "/bin/bash", "entrypoint.sh" ]