# This makefile downloads and builds the boost library

# support for building boost independently, normally these variables are set
# in the parent makefile but this makefile can also work independently
ifeq ($(BOOST_VER_MINOR),)
BOOST_VER_MAJOR := 1
BOOST_VER_MINOR := 70
BOOST_VER_PATCH := 0
PARALLELISM := $(shell nproc --ignore 1)
endif

BOOST_VER_WITH_DOTS    := $(BOOST_VER_MAJOR).$(BOOST_VER_MINOR).$(BOOST_VER_PATCH)
BOOST_VER_WITH_UNDERSC := $(BOOST_VER_MAJOR)_$(BOOST_VER_MINOR)_$(BOOST_VER_PATCH)
BOOST_FILENAME_NO_EXT  := boost_$(BOOST_VER_WITH_UNDERSC)

# boost generic target and link to real booster folder
boost: $(BOOST_FILENAME_NO_EXT)/build.done
	ln -s $(BOOST_FILENAME_NO_EXT) boost

# boost library download
$(BOOST_FILENAME_NO_EXT).7z:
	wget https://sourceforge.net/projects/boost/files/boost/$(BOOST_VER_WITH_DOTS)/$@

# unpacking boost library
$(BOOST_FILENAME_NO_EXT)/unpack.done: $(BOOST_FILENAME_NO_EXT).7z
	7z x $(BOOST_FILENAME_NO_EXT).7z
	touch $@

# boost library bootstrap
$(BOOST_FILENAME_NO_EXT)/bootstrap.done: $(BOOST_FILENAME_NO_EXT)/unpack.done
	cd $(BOOST_FILENAME_NO_EXT) && ./bootstrap.sh --without-libraries=python
	touch $@

# build boost library
$(BOOST_FILENAME_NO_EXT)/build.done: $(BOOST_FILENAME_NO_EXT)/bootstrap.done
	cd $(BOOST_FILENAME_NO_EXT) && ./b2 -j$(PARALLELISM)
	touch $@
