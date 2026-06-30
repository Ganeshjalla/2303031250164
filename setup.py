from setuptools import setup, find_packages

setup(
    name="logging_middleware",
    version="0.1.0",
    description="Reusable logging middleware that posts structured logs to the Test Server",
    packages=find_packages(),
    install_requires=["requests"],
    python_requires=">=3.8",
)
