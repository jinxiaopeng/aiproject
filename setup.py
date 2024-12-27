from setuptools import setup, find_packages

setup(
    name="ctf-platform",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "mysql-connector-python",
        "python-jose[cryptography]",
        "passlib[bcrypt]",
        "python-multipart",
        "psutil"
    ]
) 