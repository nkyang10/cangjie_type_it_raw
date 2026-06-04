# Contributing

Thanks for your interest in contributing to **Cangjie Type It Raw**!

## How to Contribute

### Reporting Issues

Found a bug or have a suggestion? [Open an issue](https://github.com/nkyang10/cangjie_type_it_raw/issues/new) with:

- A clear description
- Steps to reproduce (if bug)
- Expected vs actual behaviour

### Code Contributions

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/my-feature`
3. **Develop** your changes
4. **Test** with `python -m pytest`
5. **Commit** with a clear message
6. **Push** and open a Pull Request

### Development Setup

```bash
git clone https://github.com/nkyang10/cangjie_type_it_raw.git
cd cangjie_type_it_raw
pip install -e ".[dev]"
```

### Running Tests

```bash
# Basic tests
python -m pytest

# With coverage
python -m pytest --cov=cj_decoder --cov-report=term-missing

# All Python versions (requires tox)
tox
```

### Code Style

- Target Python 3.8+
- Follow PEP 8
- Type hints are appreciated but not required
- 100+ character line length is fine where clarity benefits

### Pull Request Guidelines

- Keep changes focused — one PR = one feature/fix
- Add tests for new functionality
- Update CHANGELOG.md under "Unreleased"
- Verify the CI pipeline passes

## Adding Dictionary Entries

The dictionary comes from [Cangjie3-Plus](https://github.com/Arthurmcarthur/Cangjie3-Plus).
If you find missing or incorrect codes, please contribute upstream.

For temporary custom entries, use the `--dict` flag with your own dictionary file.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
