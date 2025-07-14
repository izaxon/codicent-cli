@echo off
echo Testing upload to Test PyPI first...
echo You'll need your Test PyPI token
C:/Users/johan/AppData/Local/Programs/Python/Python312-arm64/python.exe -m twine upload --repository testpypi dist/*

echo.
echo If test upload was successful, upload to production PyPI:
echo You'll need your PyPI token
C:/Users/johan/AppData/Local/Programs/Python/Python312-arm64/python.exe -m twine upload dist/*
