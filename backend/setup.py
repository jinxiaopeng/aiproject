from setuptools import setup, find_packages

setup(
    name="monitor_service",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "requests",
        "python-multipart",
    ],
) 