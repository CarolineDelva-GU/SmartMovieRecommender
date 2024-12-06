import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()
    
setuptools.setup(
    name='matcher',
    version='0.0.1',
    author='Caroline Delva Lizzie Healy Rachna Rawalpally',
    author_email='cd1338@georgetown.edu',
    description='brief description',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    extras_requres={"dev": ["pytest", "flake8", "autopep8"]},
)
