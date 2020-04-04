import setuptools

# Packaging Reference:
# https://packaging.python.org/tutorials/packaging-projects/
# python setup.py sdist bdist_wheel
# python -m twine upload dist/*


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SysMPy",
    version="0.0.10",
    author="SysMPy Team",
    license="Apache License Version 2.0",
    author_email="pcyoung75@gmail.com",
    description="A library for System Modeling Runtime Environment (SMRE)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pcyoung75/SysMPy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)