import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='human_name_compare',
    version='0.1.1',
    scripts=['hn-compare'],
    author="Robert Schoenthal",
    author_email="robert.schoenthal@gmail.com",
    description="a tool for comparing human names",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/digitalkaoz/py_human_name_compare",
    download_url="https://github.com/digitalkaoz/py_human_name_compare/archive/0.1.tar.gz",
    packages=setuptools.find_packages(),
    keywords=['NLP', 'HUMANNAME'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
