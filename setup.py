import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='human-name-compare',
    version='0.3.13',
    scripts=['hn-compare'],
    author="Robert Schoenthal",
    author_email="robert.schoenthal@gmail.com",
    description="a tool for comparing human names",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/digitalkaoz/py_human_name_compare",
    download_url="https://github.com/digitalkaoz/py_human_name_compare/archive/0.3.13.tar.gz",
    packages=['human_name_compare'],
    package_dir={'human_name_compare': 'human_name_compare'},
    keywords=['NLP', 'HUMANNAME'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
