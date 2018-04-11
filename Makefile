#
# Red Pitaya specific application Makefile.
#

APP=dummy

-include _settings.env
-include _build_number

# If you want to set specific variables use the file: settings.env
#
# i.e.

# Versioning system
REVISION ?= devbuild
VER:=$(shell cat $(APP)/info/info.json | grep version | sed -e 's/.*:\ *\"//' | sed -e 's/-.*//')

INSTALL_DIR ?= .

folder=$(CURDIR:%/=%)


CFLAGS += -DVERSION=$(VER)-$(BUILD_NUMBER) -DREVISION=$(REVISION)
export CFLAGS


.PHONY: clean upload

all:
	$(MAKE) -C $(APP) all
	$(MAKE) -C $(APP) zip
	$(MAKE) -C $(APP) tar

clean:
	$(MAKE) -C $(APP) clean

upload:
	$(MAKE) -C $(APP) upload
