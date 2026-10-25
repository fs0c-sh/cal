from setuptools import setup, find_packages

setup(
    name="cal",
    version="1.3.0",
    description="Personal calendar CLI with server sync",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="fs0c",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=["Jinja2>=3.0"],
    entry_points={"console_scripts": ["calendar = calendar.cli:main"]},
)
