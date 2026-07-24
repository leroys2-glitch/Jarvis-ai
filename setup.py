from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="jarvis-ai",
    version="0.1.0",
    author="Leroy Moens",
    author_email="leroymoens2@gmail.com",
    description="An intelligent AI assistant inspired by Iron Man's Jarvis system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/leroys2-glitch/Jarvis-ai",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=[
        "nltk>=3.8.1",
        "spacy>=3.7.2",
        "transformers>=4.35.2",
        "torch>=2.1.1",
        "SpeechRecognition>=3.10.0",
        "pyttsx3>=2.90",
        "requests>=2.31.0",
        "numpy>=1.24.3",
        "pandas>=2.1.3",
        "PyYAML>=6.0.1",
    ],
    entry_points={
        "console_scripts": [
            "jarvis=jarvis.cli:main",
        ],
    },
)
