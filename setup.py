from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ai-code-debugger",
    version="0.1.1",
    author="Ajitesh",
    author_email="ajiteshleo@gmail.com",
    description="Automatically debug code from your terminal using AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/samarthaggarwal/always-on-debugger",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "anthropic",
        "python-dotenv"
    ],
    entry_points={
        'console_scripts': [
            'debug=aidebug.terminal:main',
        ],
    },
) 