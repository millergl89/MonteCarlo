from setuptools import setup, find_packages

setup(
    name='montecarlo-simulator',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.21',
        'pandas>=1.3'
    ],
    author='Greg Miller',
    description='A Monte Carlo simulation framework with dice games',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/montecarlo-simulator',  # optional
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)