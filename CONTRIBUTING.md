# Contributing

Contributions are welcome for scenario packs, adapters, scoring checks and documentation.

A scenario contribution must include a business objective, explicit mutation boundary, deterministic checks, evidence classification, license-compatible fixtures and a passing/failing proposal pair. Do not include customer data, credentials or claims that cannot be reproduced.

Run `python -m pip install -e . && python -m unittest discover -s tests -p 'test_unittest.py' -v` before opening a pull request.
