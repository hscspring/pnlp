
.PHONY: build
build:
	python3.8 setup.py sdist bdist_wheel

.PHONY: upload
upload:
	python3.8 -m twine upload -r pypi dist/*

.PHONY: clean
clean:
	rm -rf ./dist/ ./build/ ./pnlp.egg-info/
