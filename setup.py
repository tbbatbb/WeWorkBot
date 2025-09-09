
import setuptools

long_description = '''
Please refer to the homepage of the library
'''

setuptools.setup(
  name="wwbot",
  version="0.0.16",
  author="tbbatbb",
  author_email="20682299+tbbatbb@users.noreply.github.com",
  description="A library for dealing with messages in WeWork",
  url="https://github.com/tbbatbb/WeWorkBot",
  long_description_content_type='text/markdown',
  long_description=long_description,
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
