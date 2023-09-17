from setuptools import setup, find_packages
import sys
import platform
import os

if sys.version_info < (2, 7):
    raise OSError("Can't run in Python < 2.7")
elif sys.version_info > (3, 0) and sys.version_info <= (3, 3):
    raise OSError("We don't support this far back")


requires = [
    "paramiko",
    "pyperclip",
    "click"
]

if sys.version_info < (3, 5):
    requires.append("typing")

version = "0.1.0"

if os.path.exists("VERSION"):
    with open("VERSION", "r", encoding="utf-8") as f:
        version = f.read().strip()

if "VERSION" in os.environ:
    version = os.environ.get("VERSION")

setup(
    name="sshclip",
    version=version,
    license="Apache 2.0",
    author="tris10au",
    description="TODO",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    entry_points="""
        [console_scripts]
        sshclip=sshclip:cli
    """,
    extras_require={
        ':platform_system=="Darwin"': [
            "pyobjc"
        ]
    }
)
