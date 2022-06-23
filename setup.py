from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

REQUIRES_PYTHON = ">=3.6.0"
REQUIRED = ["numpy<1.22,<2", "pandas>=1,<2", "google-cloud", "gcsfs"]

setup(
    name="hvzn",
    packages=find_packages(),
    version="0.1.0",
    description="hvzn tools",
    long_description=long_description,
    python_requires=REQUIRES_PYTHON,
    install_requires=REQUIRED,
    extras_require={},
)
