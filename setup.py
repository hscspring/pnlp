import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pnlp",
<<<<<<< HEAD
    version="0.3.6",
=======
    version="0.3.7",
>>>>>>> c053a621edbe09686b42e4e9f6df97cf913b85b3
    author="Yam",
    author_email="haoshaochun@gmail.com",
    description="A pre-processing tool for NLP.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hscspring/pnlp",
    include_package_data=True,
    # default is `setup.py` path, so do not need a `package_dir` attr
    # if another dir, should be declared by `package_dir`
    packages=setuptools.find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=[
        'addict',
        'pyyaml',
        'numpy'
    ],
    package_data={
        'pnlp': ["stopwords/*"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
