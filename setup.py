from setuptools import setup

setup(
    name="data_validation",
    version="1.0.0",
    description="Utilities for data validation",
    author="Jairus Martinez",
    author_email="jairus.martinez@curaleaf.com",
    packages=["data_validation"],
    install_requires=[
        "pandas",
        "numpy"
    ],
    python_requires=">=3.12",
)