VERSION := 0.9.3
PACKAGES := tgcurses/*.py \
		    tgcurses/canvas/*.py \
		    tgcurses/layout/*.py \
		    tgcurses/ui/*.py
PYTHON := python3

.PHONY: all
all: tgcurses

.PHONY: clean
clean:
	rm -rf dist tgcurses.egg-info build

.PHONY: tgcurses
tgcurses: dist/tgcurses-$(VERSION)-py3-none-any.whl

.PHONY: install
install: tgcurses
	sudo $(PYTHON) -m pip install --force-reinstall dist/tgcurses-$(VERSION)-py3-none-any.whl

.PHONY: uninstall
uninstall:
	sudo $(PYTHON) -m pip uninstall tgcurses

dist/tgcurses-$(VERSION)-py3-none-any.whl: setup.py setup.cfg $(PACKAGES)
	$(PYTHON) setup.py sdist bdist_wheel
