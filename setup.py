from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(name='whatchamacallit',
    version='0.0.6',
    description='Use web resources the pythonic way, import JavaScript modules like you do with Python modules.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Wolfgang Kühn',
    author_email=None,
    maintainer='Wolfgang Kühn',
    maintainer_email=None,
    url='https://github.com/decatur/whatchamacallit',
    packages=['whatchamacallit', 'whatchamacallit.examples'],
    package_data={'': ['*']},
    extras_require={':python_version < "3.9"': ['importlib-resources>=3.0,<4.0']},
    python_requires='>=3.6,<4.0',)
