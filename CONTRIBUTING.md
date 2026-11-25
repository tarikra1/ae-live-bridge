# Contributing to ae-live-bridge

1. Fork and clone the repository.
2. Install in editable mode (`pip install -e .`) and run unit tests:
   ```bash
   python -m unittest discover -s tests -v
   ```
3. Ensure ExtendScript expressions remain single-line and use `.tmp` atomic staging before `os.replace`.
