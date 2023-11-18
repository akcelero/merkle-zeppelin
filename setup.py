from setuptools import find_packages, setup

requirements = ["pycryptodome>=3.0.0", "eth-abi>=4.0.0"]

pydantic_requirements = ["pydantic>=2.0.0"]

tests_requirements = ["pytest-cov>=4.0.0", "pytest>=7.0.0"]

all_requirements = pydantic_requirements


VERSION = "0.1.0"
DESCRIPTION = "MerkleTree implementation"
LONG_DESCRIPTION = "Yet another package for MerkleTree, this time compatible with OpenZeppelin implementation"

setup(
    name="merkle-zeppelin",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="akcelero",
    author_email="akcelero@gmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires=requirements,
    tests_requires=tests_requirements,
    keywords="merkle tree merkletree openzeppelin",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
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
