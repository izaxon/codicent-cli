from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop
import sys
import subprocess
import warnings

# Read README for long description
try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "Command-line interface for the Codicent API"

def check_codicent_py():
    """
    Check if codicent-py can be imported, and provide helpful error messages if not.
    This runs after installation to validate the setup.
    """
    try:
        import codicentpy
        print("✅ codicent-py imported successfully")
        return True
    except ImportError as e:
        warnings.warn(
            f"Warning: codicent-py could not be imported after installation: {e}\n"
            f"If you encounter import errors, try installing manually:\n"
            f"  pip install codicent-py"
        )
        return False

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        # Run the check in a separate process to ensure it uses the installed packages
        try:
            subprocess.check_call([sys.executable, '-c', 
                'try:\n'
                '    import codicentpy\n'
                '    print("✅ Codicent CLI installation successful - all dependencies available")\n'
                'except ImportError as e:\n'
                '    print(f"⚠️  Warning: codicent-py import failed: {e}")\n'
                '    print("💡 If you encounter issues, try: pip install codicent-py")'
            ])
        except subprocess.CalledProcessError:
            print("⚠️  Could not verify codicent-py installation")

class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        develop.run(self)
        # Same check for development install
        try:
            subprocess.check_call([sys.executable, '-c', 
                'try:\n'
                '    import codicentpy\n'
                '    print("✅ Codicent CLI development installation successful")\n'
                'except ImportError as e:\n'
                '    print(f"⚠️  Warning: codicent-py import failed: {e}")\n'
                '    print("💡 For development, try: pip install codicent-py")'
            ])
        except subprocess.CalledProcessError:
            print("⚠️  Could not verify codicent-py installation")

setup(
    name='codicent-cli',
    version='0.4.7',
    author='Johan Isaksson',
    author_email='johan@izaxon.com',
    description='Command-line interface for the Codicent API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/izaxon/codicent-cli',
    project_urls={
        'Bug Reports': 'https://github.com/izaxon/codicent-cli/issues',
        'Source': 'https://github.com/izaxon/codicent-cli',
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    keywords='codicent cli api chat ai',
    py_modules=['app', 'auth'],
    python_requires='>=3.6',
    install_requires=[
        'rich>=10.0.0',
        'codicent-py>=1.0.0',
        'prompt_toolkit>=3.0.0',
        'requests>=2.20.0'
    ],
    entry_points={
        'console_scripts': [
            'codicent=app:main',
        ],
    },
    cmdclass={
        'install': PostInstallCommand,
        'develop': PostDevelopCommand,
    },
)
