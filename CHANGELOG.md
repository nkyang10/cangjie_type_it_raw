# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] — 2026-06-04

### Added
- Initial public release
- Cangjie code → Chinese character decoding (Cangjie 3rd generation)
- Smart tokenizer with English/numbers/punctuation passthrough
- Context-aware classification of short ambiguous tokens (e.g. "a", "am", "in")
- Fuzzy typo matching via SequenceMatcher with configurable threshold
- Interactive decoding mode (`--interactive`)
- Single code lookup with radical breakdown and Unicode info (`--lookup`)
- Verbose mode showing fuzzy match warnings (`--verbose`)
- Custom dictionary support (`--dict`)
- pip-installable package with `cj-decode` CLI entry point
- Comprehensive README in English and Traditional Chinese (Hong Kong)
- GitHub Actions CI with linting, testing, and release automation
- 116K+ entry dictionary from Cangjie3-Plus (MIT License)
- Example test suite with pytest
