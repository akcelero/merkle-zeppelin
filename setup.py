import pathlib

from setuptools import find_packages, setup

requirements = ["pycryptodome>=3.0.0", "eth-abi>=4.0.0"]

pydantic_requirements = ["pydantic>=2.0.0"]

tests_requirements = ["pytest-cov>=4.0.0", "pytest>=7.0.0"]

all_requirements = pydantic_requirements


# Load the package's metadata from __version__.py
here = pathlib.Path(__file__).parent.resolve()
about: dict[str, str] = {}
with (here / "merkle_zeppelin" / "__version__.py").open() as f:
    exec(f.read(), about)

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")


setup(
    name=about["__name__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=about["__author__"],
    author_email=about["__email__"],
    url=about["__url__"],
    license="MIT",
    packages=find_packages(),
    package_data={
        # PEP-0561: https://www.python.org/dev/peps/pep-0561/#packaging-type-information
        "merkle_zeppelin": ["py.typed"],
    },
    install_requires=requirements,
    tests_requires=tests_requirements,
    keywords="merkle tree merkletree openzeppelin",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Utilities",
    ],
    extras_require={
        "all": all_requirements,
        "test": all_requirements + tests_requirements,
        "pydantic": pydantic_requirements,
    },
)
