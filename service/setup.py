from setuptools import find_packages, setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='cursion',
    version='0.0.5',
    packages=find_packages(),
    install_requires=[
        'python-dotenv',
        'requests',
        'rich',
        'typer',
    ],
    entry_points={
        'console_scripts': [
            'cursion=src.cursion.root:root'
        ]
    },
    long_description=long_description,
    long_description_content_type='text/markdown'
)
