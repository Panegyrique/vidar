from setuptools import setup, find_packages
import os

setup(
    name="vidar",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.26.4",
        "tqdm>=4.67.1",
        "scared>=1.1.4",
        "pandas>=2.2.3",
        "plotly>=5.24.1",
        "dash>=2.18.2",
    ],
    author="Panegyrique",
    description="Vidar - Side Channel Analysis Tools",
    long_description=open("README.md").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    url="https://github.com/Panegyrique/vidar",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Security :: Cryptography",
    ],
    python_requires=">=3.6",
)
