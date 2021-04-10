BOOST_VER_MAJOR := 1
BOOST_VER_MINOR := 72
BOOST_VER_PATCH := 0
BOOST_VER_WITH_DOTS    := $(BOOST_VER_MAJOR).$(BOOST_VER_MINOR).$(BOOST_VER_PATCH)
BOOST_VER_WITH_UNDERSC := $(BOOST_VER_MAJOR)_$(BOOST_VER_MINOR)_$(BOOST_VER_PATCH)
BOOST_FILENAME_NO_EXT  := boost_$(BOOST_VER_WITH_UNDERSC)

PARALLELISM := 8

NANO_BRANCH := V21.3

default: nano-build

# boost library download
$(BOOST_FILENAME_NO_EXT).7z:
	wget https://sourceforge.net/projects/boost/files/boost/$(BOOST_VER_WITH_DOTS)/$@

# unpacking boost library
$(BOOST_FILENAME_NO_EXT)/unpack.done: $(BOOST_FILENAME_NO_EXT).7z
	7z x $(BOOST_FILENAME_NO_EXT).7z
	touch $@

# boost library bootstrap
$(BOOST_FILENAME_NO_EXT)/bootstrap.done: $(BOOST_FILENAME_NO_EXT)/unpack.done
	cd $(BOOST_FILENAME_NO_EXT) && ./bootstrap.sh
	touch $@

# build boost library
$(BOOST_FILENAME_NO_EXT)/build.done: $(BOOST_FILENAME_NO_EXT)/bootstrap.done
	cd $(BOOST_FILENAME_NO_EXT) && ./b2 -j$(PARALLELISM)
	touch $@

# boost generic target and link to real booster folder
boost: $(BOOST_FILENAME_NO_EXT)/build.done
	ln -s $(BOOST_FILENAME_NO_EXT) boost

# clone nano-node github project recirsively and checkout a particular branch
git.clone.done:
	git clone --branch $(NANO_BRANCH) --recursive https://github.com/nanocurrency/nano-node.git
	touch $@

BOOST_ROOT := $(CURDIR)/$(BOOST_FILENAME_NO_EXT)
export BOOST_ROOT

# build the nano node
# TODO: this target should ideally split into smaller targets
nano-build: git.clone.done boost
	mkdir -p nano-build data
	cd nano-build && cmake -G "Unix Makefiles" -DNANO_TEST=ON -DCMAKE_BUILD_TYPE=Debug ../nano-node
	cd nano-build && $(MAKE) -j$(PARALLELISM)
	#cd nano-build && ./nano_node --diagnostics --data_path ../data

# download a copy of the latest ledger and check the hash then inflate it
# SECURITY RISK: this step is not secure and not recomended for proper nodes
get_ledger:
	mkdir -p ledgercache
	cd ledgercache && wget https://mynano.ninja/api/ledger/checksum/sha256 -O data.ldb.sha256
	cd ledgercache && wget -O data.ldb.7z https://mynano.ninja/api/ledger/download
	cd ledgercache && echo `cat data.ldb.sha256` data.ldb.7z | sha256sum --check
	cd ledgercache && 7z x data.ldb.7z

# force the downloaded ledger into data/data.ldb
force_ledger:
	cp ledgercache/data.ldb data/data.ldb

# run nano node using a local data directory
run_node:
	cd nano-build && ./nano_node --daemon --config rpc.enable=true --data_path ../data

# tail all the log files
tail_logs:
	tail -f data/log/*

# rpc enable control
enable_control:
	echo "enable_control = true" > data/config-rpc.toml

.PHONY: force_ledger run_node tail_logs nano-build enable_control
