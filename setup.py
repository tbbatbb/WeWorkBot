
import setuptools

with open("readme.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="wwbot",
  version="0.0.1",
  author="tbbatbb",
  author_email="20682299+tbbatbb@users.noreply.github.com",
  description="A library for dealing with messages in WeWork",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/tbbatbb/WeWorkBot",
  packages=setuptools.find_packages(),
  classifiers=[
    "Development Status :: 2 - Pre-Alpha",
    "Framework :: Flask",
    "Intended Audience :: Developers",
    "License :: Free for non-commercial use",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Programming Language :: Python :: Implementation :: CPython",
    "Topic :: Communications :: Chat",
    "Topic :: Software Development :: Libraries :: Python Modules"
  ],
)
