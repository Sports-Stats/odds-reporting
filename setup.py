from setuptools import find_packages
from setuptools import setup

main_ns = {}
with open("version.py") as f:
    exec(f.read(), main_ns)

setup(
    name="odds_reporting",
    version=main_ns["__version__"],
    packages=find_packages(),
    include_package_data=True,
    install_requires=["pandas", "requests"],
)
