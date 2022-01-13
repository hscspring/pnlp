
.PHONY: build
build:
	python3.8 setup.py sdist bdist_wheel

.PHONY: upload
upload:
	python3.8 -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

.PHONY: clean
clean:
	rm -rf ./dist/ ./build/ ./pnlp.egg-info/
