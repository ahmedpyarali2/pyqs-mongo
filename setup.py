import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyqs-mongo",
    version="0.0.1",
    author="Ahmed Pyar Ali",
    author_email="ahmed.dhanani26@gmail.com",
    description="A useful tool to parse the query string parameters on a resource into a MongoDB query object "
                "(compatible with PyMongo and MongoEngine).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mrpycharm/pyqs-mongo",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
