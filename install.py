#!/usr/bin/env python
import argparse
import os
import subprocess
import sys


def main(environment, packages):
    if environment == "test":
        subprocess.call(f"pip install .", shell=True)

    if packages:
        subprocess.call(f"pip install {' '.join(packages)}", shell=True)
    else:
        print("Upgrading pip...")
        subprocess.call("python -m pip install --upgrade pip", shell=True)
        subprocess.call("python -m pip install wheel", shell=True)
        if environment == "dist":
            subprocess.call("pip install .", shell=True)
        else:
            subprocess.call("pip install -e .", shell=True)
            subprocess.call("pip install pre-commit pylint", shell=True)
            subprocess.call("pre-commit install", shell=True)
            subprocess.call("pre-commit run --all-files", shell=True)


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()

    PARSER.add_argument(
        "-e",
        "--env",
        help="Environment that is being configured",
        default="local",
        choices=["local", "dist", "test"],
    )

    PARSER.add_argument(
        "-p",
        "--packages",
        help="Python packages to be installed",
        metavar="packages",
        nargs="*",
    )

    ARGS = PARSER.parse_args()
    main(ARGS.env, ARGS.packages)
