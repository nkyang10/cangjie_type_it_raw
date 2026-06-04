"""Verify the Cangjie dictionary is loadable and has expected entries."""
import sys

sys.path.insert(0, ".")
from cj_decoder import load_dictionary

code_to_chars, char_to_codes = load_dictionary("cj3.txt")
print(f"Loaded {len(code_to_chars)} codes, {len(char_to_codes)} characters")
assert len(code_to_chars) > 50000, "Dictionary too small"
assert "onf" in code_to_chars, "Missing 你 (onf)"
assert "okr" in code_to_chars, "Missing 知 (okr)"
print("Dictionary validation passed")
