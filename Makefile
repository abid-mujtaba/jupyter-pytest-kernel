.PHONY: install list run

run: install list
	jupyter notebook
	
install:
	jupyter kernelspec install --user pytest

list:
	jupyter kernelspec list
