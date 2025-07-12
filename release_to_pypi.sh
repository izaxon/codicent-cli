# PyPI Release Script for Codicent CLI
# Run this script to build and upload to PyPI

# 1. Install build tools
pip install build twine

# 2. Clean previous builds
rm -rf dist/ build/ *.egg-info/

# 3. Build the package
python -m build

# 4. Check the build
python -m twine check dist/*

# 5. Upload to PyPI (you'll need PyPI credentials)
# Test PyPI first:
# python -m twine upload --repository testpypi dist/*

# Production PyPI:
# python -m twine upload dist/*
