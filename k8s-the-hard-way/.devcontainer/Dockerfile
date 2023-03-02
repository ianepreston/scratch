FROM ianepreston/iac-devcontainer

# Install cfssl for cert creation
RUN export DEBIAN_FRONTEND=noninteractive && \
	apt update && \
	apt install -y golang && \
	mkdir -p /go && \
	export GOPATH=/go && \
	go install github.com/cloudflare/cfssl/cmd/...@latest && \
	chmod -R 777 /go

ENV PATH "$PATH:/go/bin"