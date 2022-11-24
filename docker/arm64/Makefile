# This dockerfile defines 2 dockers:
# nano_node_base_tools_arm64, which has the software tools need to compile
# dsiganos/nano_node_arm64, which has the compiled executable that can be run

TAG  := dsiganos/nano_node_arm64:latest
TAG2 := dsiganos/nano_node_base_tools_arm64:0.1

ENABLE_CONTROL := --rpcconfig enable_control=true
ENABLE_RPC := --config rpc.enable=true
LOG_TO_CERR := --config node.logging.log_to_cerr=true
RPC_ADDR := --rpcconfig address=::
WEBSOCKET_ENABLE := --config node.websocket.enable=true
WEBSOCKET_ADDR := --config node.websocket.address=::
CONFIG_ARGS := $(ENABLE_CONTROL) $(ENABLE_RPC) $(LOG_TO_CERR) $(RPC_ADDR) $(WEBSOCKET_ADDR) $(WEBSOCKET_ENABLE)

build-base-tools-arm64:
	docker build --progress plain -f Dockerfile-base-tools-arm64 -t $(TAG2) ../..

shell:
	docker run -it $(TAG) bash

rootshell:
	docker run -u 0 -it $(TAG) bash

build:
	docker build --progress plain -f Dockerfile-arm64 -t $(TAG) ../..

run_live:
	docker run --restart=unless-stopped -d \
        -p 7075:7075 \
        -p 7076:7076 \
        -p 7078:7078 \
        -v livedata:/root \
        --name nano_node_live \
        ${TAG} \
        nano_node --daemon $(CONFIG_ARGS) --network live

run_beta:
	docker run --restart=unless-stopped -d \
        -p 54000:54000 \
        -p 55000:55000 \
        -p 57000:57000 \
        -v betadata:/root \
        --name nano_node_beta \
        ${TAG} \
        nano_node --daemon $(CONFIG_ARGS) --network beta

run_test:
	docker run --restart=unless-stopped -d \
        -p 17075:17075 \
        -p 17076:17076 \
        -p 17078:17078 \
        -v testdata:/root \
        --name nano_node_test \
        ${TAG} \
        nano_node --daemon $(CONFIG_ARGS) --network test

push:
	docker push $(TAG)

.PHONY: default shell build build-base-tools-arm64 run push
