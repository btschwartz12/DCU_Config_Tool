rmdir /S /Q dist 2>nul
rmdir /S /Q build 2>nul
:: https://stackoverflow.com/questions/28991015/python3-project-remove-pycache-folders-and-pyc-files
python -Bc "import pathlib; [p.unlink() for p in pathlib.Path('.').rglob('*.py[co]')]"
python -Bc "import pathlib; [p.rmdir() for p in pathlib.Path('.').rglob('__pycache__')]"

:: del *.spec 2>nul