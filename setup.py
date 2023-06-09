import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='yargy_extraction_wrapper',
    version='0.0.1',
    author='al3xk0s',
    author_email='bebe558812@gmail.com',
    description='Colab wrapper for yargy',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/al3xk0s/yargy_extraction_wrapper',
    project_urls = {
        "Bug Tracker": "https://github.com/al3xk0s/yargy_extraction_wrapper/issues"
    },
    license='MIT',
    packages=['toolbox'],
    install_requires=['requests'],
)
