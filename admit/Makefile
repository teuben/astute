#
#


SITE = teuben@chara.astro.umd.edu:public_html/admit/dist
URL  = http://www.astro.umd.edu/~teuben/admit/dist
VERSION = 0.0.3
PY = 2.7

# locally at UMD:  /local/ftp/pub/carma/data/admit/
FTP = ftp.astro.umd.edu:pub/carma/data/admit/


help:
	@echo Reminders/Helpers to build/distribute ADMIT:
	@echo "SITE     = $(SITE)"
	@echo "CASAPATH = $(CASAPATH)"
	@echo "VERSION  = $(VERSION)"
	@echo "PY       = $(PY)"
	@echo "URL      = $(URL)/admit-$(VERSION)-py$(PY).egg"
	@echo "targets:"
	@echo "  build                               build the egg"
	@echo "  dist                                scp egg to SITE"
	@echo "  install"
	@echo "  import (temp)"
	@echo "  casa (uses PP and CASAPATH)"
	@echo "  home (uses HP and HOME/python/)"


.PHONY:  build dist 

clean:
	@echo No clean yet....

build:
	python setup.py bdist_egg

dist:
	scp dist/admit-$(VERSION)-py$(PY).egg $(SITE)

install:
	@echo "Pick one of the following (you may need to prepend with 'sudo'):"
	@echo " install_local"
	@echo " install_url"

install_local:
	easy_install dist/admit-$(VERSION)-py$(PY).egg

install_url:
	easy_install $(URL)/admit-$(VERSION)-py$(PY).egg

# special install (both lib/ and python/ can be symlinks to the right version)
PP = $(CASAPATH)/lib/python/site-packages/ 

casa:
	@if [ -d $(PP) ]; then \
	  PYTHONPATH=$(PP) easy_install --prefix=$(CASAPATH) dist/admit-$(VERSION)-py$(PY).egg; \
	else \
	  echo PYTHONPATH PP=$(PP) does not seem to exist;\
	  echo CASAPATH=$(CASAPATH) also needs to be set;\
	  echo Cannot easy_install ADMIT this way.;\
	fi

ls1:
	ls $(PP)
	@echo "PP=$(PP)"

MYPYTHON = $(HOME)/python

HP = $(MYPYTHON)/lib/python$(PY)/site-packages

home:
	@if [ -d $(HP) ]; then \
	  PYTHONPATH=$(HP) easy_install --prefix=$(MYPYTHON) dist/admit-$(VERSION)-py$(PY).egg; \
	else \
	  @echo PYTHONPATH PP=$(PP) does not seem to exist. Cannot easy_install ADMIT.;\
	fi

ls2:
	ls $(HP)
	@echo "HP=$(HP)"


#  danger, borrow from ASTUTE
FILES = adm.py parfile.py

export:
	@echo There is no export, only import from astute for now

import:
	(cd admit; for i in $(FILES); do cp ../../lib/$$i .; done)

diff:
	(cd admit; for i in $(FILES); do diff $$i ../../lib/; done)
	(cd admit; for i in $(FILES); do ls -l $$i ../../lib/$$i; done)




#  quick access to datasets

data:
	mkdir -p data

# 

bench1:	data data/bench1

data/bench1:
	(cd data; wget -O - $(FTP)/bench1.tar.gz | tar zxf -)

test1: bench1
	python tests/test1.py

# 
bench2:	data data/bench2

data/bench2:
	(cd data; wget -O - $(FTP)/bench2.tar.gz | tar zxf -)

test2: bench2
	python tests/test2.py

