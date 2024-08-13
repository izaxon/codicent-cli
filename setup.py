from setuptools import setup, find_packages

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name='codicent',
    version='0.2',
    py_modules=['app'],
    install_requires=required,
    entry_points='''
        [console_scripts]
        codicent=app:main
    ''',
)
