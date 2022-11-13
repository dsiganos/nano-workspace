# This dockerfile defines 2 dockers:
# nano_node_base_tools_arm64, which has the software tools need to compile
# dsiganos/nano_node_arm64, which has the compiled executable that can be run

TAG  := dsiganos/nano_node_arm64:latest
TAG2 := dsiganos/nano_node_base_tools_arm64:0.1

shell:
	docker run -it $(TAG) bash

rootshell:
	docker run -u 0 -it $(TAG) bash

build:
	docker build --progress plain -f Dockerfile-arm64 -t $(TAG) ../..

build-base-tools-arm64:
	docker build --progress plain -f Dockerfile-base-tools-arm64 -t $(TAG2) ../..

run:
	docker run --restart=unless-stopped -d \
        -p 7075:7075 \
        -p 127.0.0.1:7076:7076 \
        -p 127.0.0.1:7078:7078 \
        -v data:/root \
        --name nano_node \
        ${TAG}

push:
	docker push $(TAG)

.PHONY: default shell build build-base-tools-arm64 run push
