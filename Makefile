# Makefile for building a nano node from scratch on linux
#
# For Ubuntu 20.04, install these packages first:
# apt-get install make cmake git p7zip-full g++ qt5-default

BOOST_VER_MAJOR := 1
BOOST_VER_MINOR := 80
BOOST_VER_PATCH := 0
export BOOST_VER_PATCH
export BOOST_VER_MAJOR
export BOOST_VER_MINOR

ifeq ($(shell uname),Darwin)
PARALLELISM := $(shell sysctl -n hw.logicalcpu)
else
PARALLELISM := $(shell nproc --ignore 1)
endif
export PARALLELISM

NANO_REPO   := https://github.com/nanocurrency/nano-node.git
NANO_BRANCH := develop

BUILDDIR := build
DATAPATH := data
NETNAME  := live

default: build

# clone nano-node github project recirsively and checkout a particular branch
git.clone.done:
	git clone --branch $(NANO_BRANCH) --recursive $(NANO_REPO) nano-node
	touch $@

ifeq ($(BOOST_ROOT),)
BOOST_ROOT := $(CURDIR)/boost/boost
export BOOST_ROOT
boost:
	$(MAKE) -C boost
else
boost:
	echo "Not building local boost library, using $(BOOST_ROOT)"
endif

# build the nano node
# TODO: this target should ideally split into smaller targets
build: git.clone.done boost
	mkdir -p $(BUILDDIR) $(DATAPATH)
	cd $(BUILDDIR) && cmake \
        -G "Unix Makefiles" \
        -DNANO_STACKTRACE_BACKTRACE=OFF \
        -DNANO_GUI=ON \
        -DNANO_TEST=ON \
        -DCMAKE_BUILD_TYPE=Debug \
        ../nano-node
	cd $(BUILDDIR) && $(MAKE) -j$(PARALLELISM)
	#cd $(BUILDDIR) && ./nano_node --diagnostics --data_path ../$(DATAPATH)

# download a copy of the latest ledger and check the hash then inflate it
# SECURITY RISK: this step is not secure and not recomended for proper nodes
get_ledger:
	mkdir -p ledgercache
	cd ledgercache && wget https://mynano.ninja/api/ledger/checksum/sha256 -O data.ldb.sha256
	cd ledgercache && wget -O data.ldb.7z https://mynano.ninja/api/ledger/download
	cd ledgercache && echo `cat data.ldb.sha256` data.ldb.7z | sha256sum --check
	cd ledgercache && 7z x data.ldb.7z

# force the downloaded ledger into $(DATAPATH)/data.ldb
force_ledger:
	cp ledgercache/data.ldb $(DATAPATH)/data.ldb

# run nano node using a local data directory
run_node:
	cd $(BUILDDIR) && ./nano_node --daemon --config rpc.enable=true --data_path ../$(DATAPATH) --network $(NETNAME)

# run nano node in beta network using a local data directory "betadata"
run_node_beta:
	mkdir -p ../betadata
	cd $(BUILDDIR) && ./nano_node --daemon --config rpc.enable=true --data_path ../betadata --network beta

# run nano node in test network using a local data directory "testdata"
run_node_test:
	mkdir -p ../testdata
	cd $(BUILDDIR) && ./nano_node --daemon --config rpc.enable=true --data_path ../testdata --network test

# run nano node using a local data directory
run_wallet:
	cd $(BUILDDIR) && ./nano_wallet --config rpc.enable=true --data_path ../$(DATAPATH) --network=$(NETNAME)

# tail all the log files
tail_logs:
	tail -f $(DATAPATH)/log/*

# rpc enable control
enable_control:
	mkdir -p $(DATAPATH)
	echo "enable_control = true" > $(DATAPATH)/config-rpc.toml

enable_voting:
	mkdir -p $(DATAPATH)
	echo "[node]"               >  $(DATAPATH)/config-node.toml
	echo "enable_voting = true" >> $(DATAPATH)/config-node.toml

# target for starting vscode, vscode needs to be started from here, when using locally built boost lib,
# so that it can pick up the environment variable BOOST_ROOT, which is set further up the makefile
vscode:
	code .

# target to create code blocks project
codeblocks: git.clone.done boost
	mkdir -p $(BUILDDIR) $(DATAPATH)
	cd $(BUILDDIR) && cmake -G "CodeBlocks - Unix Makefiles" -DNANO_GUI=ON -DNANO_TEST=ON \
		-DCMAKE_BUILD_TYPE=Debug ../nano-node

.PHONY: force_ledger run_node run_node_beta run_node_test tail_logs build enable_control boost vscode
