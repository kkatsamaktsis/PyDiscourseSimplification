import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="discoursesimplification",
    version="0.0.1",
    author="Konstantinos Katsamaktsis",
    author_email="konstantinos.katsamaktsis@student.manchester.ac.uk",
    description="Discourse Simplification",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.cs.man.ac.uk/n68155kk/discoursesimplification",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)