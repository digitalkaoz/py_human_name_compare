import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='human-name-compare',
    version='0.1',
    scripts=['hn-compare'],
    author="Robert Schönthal",
    author_email="robert.schoenthal@gmail.com",
    description="a tool for comparing human names",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/digitalkaoz/py-human-name-compare",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
