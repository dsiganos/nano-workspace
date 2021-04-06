BOOST_VER_MAJOR := 1
BOOST_VER_MINOR := 69
BOOST_VER_PATCH := 0
BOOST_VER_WITH_DOTS    := $(BOOST_VER_MAJOR).$(BOOST_VER_MINOR).$(BOOST_VER_PATCH)
BOOST_VER_WITH_UNDERSC := $(BOOST_VER_MAJOR)_$(BOOST_VER_MINOR)_$(BOOST_VER_PATCH)
BOOST_FILENAME_NO_EXT  := boost_$(BOOST_VER_WITH_UNDERSC)

PARALLELISM := 8

NANO_BRANCH := V21.3

default:  nano-node/nano_node

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

# clone nano-node github project recirsively and checkout a particular branch
git.clone.done:
	git clone --branch $(NANO_BRANCH) --recursive https://github.com/nanocurrency/nano-node.git
	touch $@

BOOST_ROOT := $(CURDIR)/$(BOOST_FILENAME_NO_EXT)
export BOOST_ROOT

# build the nano node
# TODO: this target should ideally split into smaller targets
nano-node/nano_node: git.clone.done $(BOOST_FILENAME_NO_EXT)/build.done
	cd nano-node && cmake -G "Unix Makefiles" -DNANO_TEST=ON .
	cd nano-node && $(MAKE) -j$(PARALLELISM) nano_node
	cd nano-node && ./nano_node --diagnostics

# download a copy of the latest ledger and check the hash then inflate it
# SECURITY RISK: this step is not secure and not recomended for proper nodes
get_ledger:
	mkdir -p ledgercache
	cd ledgercache && wget https://mynano.ninja/api/ledger/checksum/sha256 -O data.ldb.sha256
	cd ledgercache && wget -O data.ldb.7z https://mynano.ninja/api/ledger/download
	cd ledgercache && echo `cat data.ldb.sha256` data.ldb.7z | sha256sum --check
	cd ledgercache && 7z x data.ldb.7z

# force the downloaded ledger into nano-node/data/data.ldb
force_ledger:
	cp ledgercache/data.ldb nano-node/data/data.ldb

# run nano node using a local data directory
run_node:
	cd nano-node && ./nano_node --daemon --config rpc.enable=true --data_path data

# tail all the log files
tail_logs:
	tail -f nano-node/data/log/*

.PHONY: force_ledger run_node tail_logs
