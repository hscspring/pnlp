import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pnlp",
    version="0.27",
    author="Yam",
    author_email="haoshaochun@gmail.com",
    description="A pre-processing tool for NLP.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hscspring/pnlp",
    include_package_data=True,
    packages=setuptools.find_packages(),
    install_requires=[
          'addict',
          'pyyaml',
    ],
    package_data={
        'pnlp': ["stopwords/*"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)