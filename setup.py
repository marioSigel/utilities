import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="myutilities", # Replace with your own username
    version="0.0.1",
    author="Mario Sigel",
    author_email="mario.sigel@sociovestix.com",
    description=long_description,
    long_description='Utilities',
    long_description_content_type="text/markdown",
    url="https://github.com/marioSigel/utilities",
    project_urls={
        "Bug Tracker": "https://github.com/marioSigel/utilities/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src", "cavdutils.geonames": "src/geonames"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
)