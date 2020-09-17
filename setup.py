import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mlfarm",
    version=os.environ.get('MLFARM_VERSION', '0.0.0'),
    author="Alexandru Petre",
    author_email="petre.v.alexandru@gmail.com",
    description="Tools for fast development of Machine Learning projects.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Oodapow/mlfarm/tree/release",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)