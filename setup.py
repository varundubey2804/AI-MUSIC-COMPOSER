from setuptools import setup,find_packages

with open("requirments.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="AI MUSIC COMPOSER",
    version="0.1",
    author="Varun Dubey",
    packages=find_packages(),
    install_requires = requirements,
)