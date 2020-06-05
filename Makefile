VERSION := 0.9.3
PACKAGES := tgcurses/*.py \
		    tgcurses/canvas/*.py \
		    tgcurses/layout/*.py \
		    tgcurses/ui/*.py

.PHONY: all
all: tgcurses

.PHONY: clean
clean:
	rm -rf dist tgcurses.egg-info build

.PHONY: tgcurses
tgcurses: dist/tgcurses-$(VERSION)-py3-none-any.whl

.PHONY: install
install: tgcurses
	sudo pip3 install --force-reinstall dist/tgcurses-$(VERSION)-py3-none-any.whl

.PHONY: uninstall
uninstall:
	sudo pip3 uninstall tgcurses

dist/tgcurses-$(VERSION)-py3-none-any.whl: setup.py setup.cfg $(PACKAGES)
	python3 setup.py sdist bdist_wheel
