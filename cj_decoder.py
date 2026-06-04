#!/usr/bin/env python3
"""
Cangjie Code Decoder (倉頡碼解碼器)

Decodes space-separated Cangjie input codes into Chinese characters.
Uses the Cangjie 3rd generation dictionary with fuzzy matching for typos.

Supports mixed input — English words, numbers, and punctuation pass through
unchanged while Cangjie codes are decoded in context.

Dictionary source: Cangjie3-Plus (MIT License)
  https://github.com/Arthurmcarthur/Cangjie3-Plus
"""

import sys
import os
import re
import argparse
from collections import defaultdict
from difflib import SequenceMatcher

# ── Cangjie letter-to-radical mapping ──────────────────────────────────

CANGJIE_MAP = {
    'a': '日', 'b': '月', 'c': '金', 'd': '木', 'e': '水', 'f': '火',
    'g': '土', 'h': '竹', 'i': '戈', 'j': '十', 'k': '大', 'l': '中',
    'm': '一', 'n': '弓', 'o': '人', 'p': '心', 'q': '手', 'r': '口',
    's': '尸', 't': '廿', 'u': '山', 'v': '女', 'w': '田', 'x': '難',
    'y': '卜', 'z': '（重）',
}

CANGJIE_CATEGORY = {
    '哲理類': ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
    '筆畫類': ['h', 'i', 'j', 'k', 'l', 'm', 'n'],
    '人體類': ['o', 'p', 'q', 'r'],
    '字型類': ['s', 't', 'u', 'v', 'w', 'y'],
    '難字':   ['x'],
    '重覆鍵': ['z'],
}

# Common English words that should NOT be treated as Cangjie codes
COMMON_ENGLISH = {
    'a', 'am', 'an', 'as', 'at', 'be', 'by', 'do', 'go', 'he', 'if', 'in',
    'is', 'it', 'me', 'my', 'no', 'of', 'on', 'or', 'so', 'to', 'up', 'us',
    'we', 'all', 'and', 'any', 'are', 'bad', 'big', 'but', 'can', 'did',
    'end', 'few', 'for', 'get', 'got', 'had', 'has', 'her', 'him', 'his',
    'hot', 'how', 'its', 'let', 'man', 'may', 'men', 'new', 'not', 'now',
    'old', 'one', 'our', 'out', 'own', 'put', 'ran', 'run', 'say', 'see',
    'set', 'she', 'too', 'try', 'two', 'use', 'was', 'way', 'who', 'why',
    'yes', 'yet', 'you', 'about', 'after', 'again', 'among',
    'being', 'black', 'bring', 'brown', 'build', 'could', 'doing',
    'early', 'eight', 'every', 'first', 'found', 'given', 'going',
    'great', 'green', 'group', 'heart', 'hotel', 'house', 'human',
    'large', 'later', 'learn', 'legal', 'level', 'light', 'local',
    'logic', 'might', 'money', 'month', 'moral', 'music', 'never',
    'night', 'north', 'often', 'order', 'other', 'paper', 'party',
    'peace', 'place', 'plant', 'power', 'press', 'price', 'print',
    'quick', 'quite', 'radio', 'range', 'right', 'round', 'seven',
    'shall', 'sharp', 'short', 'since', 'sixth', 'small', 'sound',
    'south', 'space', 'spend', 'stand', 'start', 'state', 'still',
    'story', 'study', 'table', 'their', 'there', 'these', 'thing',
    'think', 'third', 'those', 'three', 'today', 'total', 'touch',
    'track', 'trade', 'train', 'treat', 'under', 'unity', 'until',
    'upper', 'value', 'visit', 'voice', 'watch', 'water', 'where',
    'which', 'while', 'white', 'whole', 'whose', 'woman', 'women',
    'world', 'worry', 'would', 'write', 'wrong', 'young',
    'amazon', 'google', 'apple', 'microsoft', 'tesla', 'meta', 'netflix',
}


# ── Dictionary loading ─────────────────────────────────────────────────

def get_default_dict_path():
    """Return the path to the bundled cj3.txt dictionary."""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cj3.txt')


def load_dictionary(dict_path=None):
    """
    Load Cangjie code → character mapping from dictionary file.

    Returns (code_to_chars, char_to_codes) where:
      code_to_chars[code] -> list of characters (most common first)
      char_to_codes[char] -> set of codes
    """
    if dict_path is None:
        dict_path = get_default_dict_path()

    code_to_chars = defaultdict(list)
    char_to_codes = defaultdict(set)

    in_data = False
    with open(dict_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n\r')
            if line == '[DATA]':
                in_data = True
                continue
            if not in_data or not line.strip():
                continue

            parts = line.split(None, 1)
            if len(parts) >= 2:
                code = parts[0].strip().lower()
                char = parts[1].strip()
                code_to_chars[code].append(char)
                char_to_codes[char].add(code)

    return code_to_chars, char_to_codes


# ── Tokenizer ──────────────────────────────────────────────────────────

def is_likely_english(word):
    """Check if a token looks like a common English word or proper noun."""
    word_lower = word.lower().strip()
    if word_lower in COMMON_ENGLISH:
        return True
    if word[0].isupper() and word_lower not in {chr(i) for i in range(ord('a'), ord('z') + 1)}:
        if len(word) >= 2 and all(c.isalpha() for c in word):
            vowels = sum(1 for c in word_lower if c in 'aeiou')
            if len(word) >= 4 and vowels > 0:
                return True
    return False


def is_cangjie_code(word):
    """Check if the token looks like a valid Cangjie code sequence."""
    word = word.lower().strip()
    if len(word) > 5:
        return False
    if not word.isalpha():
        return False
    if word != word.lower():
        return False
    if is_likely_english(word):
        return False
    return True


_SHORT_AMBIGUOUS = {
    'a', 'am', 'an', 'as', 'at', 'be', 'by', 'do', 'go',
    'he', 'if', 'in', 'is', 'it', 'me', 'my', 'no', 'of',
    'on', 'or', 'so', 'to', 'up', 'us', 'we',
}


def tokenize(text):
    """
    Split input into tokens, preserving punctuation and numbers as-is.
    Uses context awareness: short ambiguous tokens between Cangjie codes
    are reclassified as Cangjie.
    """
    raw_tokens = []
    for token in text.split():
        token = token.strip()
        if not token:
            continue
        if re.match(r'^[？?！!，,。.、；;：:…—\-～~]+$', token):
            raw_tokens.append(('punct', token))
        elif re.match(r'^[0-9,.%$€£¥]+$', token):
            raw_tokens.append(('number', token))
        elif is_cangjie_code(token):
            raw_tokens.append(('cangjie', token.lower()))
        else:
            raw_tokens.append(('literal', token))

    # Context-aware correction: short ambiguous words between Cangjie codes
    tokens = list(raw_tokens)
    for i, (ttype, tval) in enumerate(tokens):
        if ttype == 'literal' and tval.lower() in _SHORT_AMBIGUOUS:
            prev_is_cangjie = i > 0 and tokens[i - 1][0] == 'cangjie'
            next_is_cangjie = i < len(tokens) - 1 and tokens[i + 1][0] == 'cangjie'
            if prev_is_cangjie or next_is_cangjie:
                tokens[i] = ('cangjie', tval.lower())

    return tokens


# ── Fuzzy matching ─────────────────────────────────────────────────────

def similarity(a, b):
    """Compute string similarity ratio (0.0–1.0)."""
    return SequenceMatcher(None, a, b).ratio()


def fuzzy_search(code, code_to_chars, threshold=0.6, max_results=5):
    """
    Find characters whose Cangjie codes are similar to the input code.
    Uses SequenceMatcher ratio matching.
    """
    candidates = []
    for known_code, chars in code_to_chars.items():
        if abs(len(known_code) - len(code)) > 3:
            continue
        score = similarity(code, known_code)
        if score >= threshold:
            for char in chars:
                candidates.append((score, known_code, char))

    candidates.sort(key=lambda x: (-x[0], x[1]))
    seen = set()
    unique = []
    for score, known_code, char in candidates:
        if char not in seen:
            seen.add(char)
            unique.append((score, known_code, char))

    return unique[:max_results]


# ── Decoding ───────────────────────────────────────────────────────────

def decode_cangjie(codes, code_to_chars):
    """
    Decode a list of Cangjie code strings into Chinese characters.

    Returns (decoded_string, errors, fuzzy_results).
    """
    result = []
    errors = []
    fuzzy_results = {}

    for code in codes:
        code = code.strip().lower()
        exact = code_to_chars.get(code)
        if exact:
            result.append(exact[0])
        else:
            candidates = fuzzy_search(code, code_to_chars)
            if candidates:
                best_score, known_code, best_char = candidates[0]
                fuzzy_results[code] = candidates
                result.append(best_char)
                errors.append(
                    f"⚠️ `{code}` → fuzzy matched `{known_code}` ≈ `{best_char}` "
                    f"(score: {best_score:.2f})"
                )
            else:
                result.append('\ufffd')
                errors.append(f"❌ `{code}` → no match found")

    return ''.join(result), errors, fuzzy_results


def decode_sentence(text, code_to_chars):
    """
    Decode a mixed sentence (Cangjie codes + English + numbers + punctuation).

    Returns (decoded_text, errors).
    """
    tokens = tokenize(text)
    result_parts = []
    errors = []

    cangjie_codes = []
    for token_type, token_value in tokens:
        if token_type == 'cangjie':
            cangjie_codes.append(token_value)
        else:
            if cangjie_codes:
                decoded, decode_errors, _ = decode_cangjie(cangjie_codes, code_to_chars)
                result_parts.append(decoded)
                errors.extend(decode_errors)
                cangjie_codes = []
            result_parts.append(token_value)

    if cangjie_codes:
        decoded, decode_errors, _ = decode_cangjie(cangjie_codes, code_to_chars)
        result_parts.append(decoded)
        errors.extend(decode_errors)

    return ''.join(result_parts), errors


# ── Interactive lookup mode ────────────────────────────────────────────

def show_code_detail(code, code_to_chars):
    """Show detailed information about a single Cangjie code."""
    code = code.lower().strip()
    exact = code_to_chars.get(code, [])

    if exact:
        lines = [f"Code: {code}"]
        radicals = ' → '.join(CANGJIE_MAP.get(c, c) for c in code)
        lines.append(f"Radicals: {radicals}")
        lines.append(f"Characters ({len(exact)}):")
        for i, ch in enumerate(exact[:20], 1):
            lines.append(f"  {i}. {ch} (U+{ord(ch):04X})")
        if len(exact) > 20:
            lines.append(f"  ... and {len(exact) - 20} more")
        return '\n'.join(lines)
    else:
        candidates = fuzzy_search(code, code_to_chars)
        if candidates:
            lines = [f"Code '{code}' not found. Did you mean?"]
            for score, known_code, char in candidates[:10]:
                radicals = ' → '.join(CANGJIE_MAP.get(c, c) for c in known_code)
                lines.append(f"  {known_code} ({radicals}) → {char}  (confidence: {score:.0%})")
            return '\n'.join(lines)
        else:
            return f"Code '{code}' not found and no similar codes available."


# ── CLI entry point ────────────────────────────────────────────────────

def build_parser():
    """Build the argument parser."""
    parser = argparse.ArgumentParser(
        description='Cangjie Code Decoder (倉頡碼解碼器)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            'Examples:\n'
            '  cj-decode onf okr rmmr okr oin a rtq mk onfd\n'
            '  echo "onf okr rmmr" | cj-decode\n'
            '  cj-decode --lookup onf\n'
            '  cj-decode --interactive\n'
        ),
    )
    parser.add_argument(
        'input', nargs='*',
        help='Text containing Cangjie codes to decode (space-separated)',
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='Show fuzzy match warnings',
    )
    parser.add_argument(
        '-l', '--lookup', metavar='CODE',
        help='Look up a single Cangjie code in detail',
    )
    parser.add_argument(
        '-i', '--interactive', action='store_true',
        help='Start interactive decoding session',
    )
    parser.add_argument(
        '-d', '--dict', metavar='PATH',
        help='Path to custom dictionary file',
    )
    parser.add_argument(
        '--version', action='store_true',
        help='Show version and exit',
    )
    return parser


def main(argv=None):
    """Main entry point."""
    if argv is None:
        argv = sys.argv[1:]

    parser = build_parser()

    # Handle --version separately
    if '--version' in argv:
        print('cj-decode v1.0.0')
        print('Dictionary: Cangjie3-Plus (MIT)')
        print('Python: ' + sys.version)
        return 0

    args = parser.parse_args(argv)

    # Resolve dictionary path
    dict_path = args.dict or get_default_dict_path()
    if not os.path.exists(dict_path):
        print(f"Error: Dictionary not found at {dict_path}", file=sys.stderr)
        return 1

    code_to_chars, _ = load_dictionary(dict_path)

    # --lookup mode
    if args.lookup:
        print(show_code_detail(args.lookup, code_to_chars))
        return 0

    # --interactive mode
    if args.interactive:
        print("Cangjie Decoder — Interactive Mode")
        print("Type Cangjie codes (space-separated). Type 'exit' or Ctrl+C to quit.")
        print("Use /lookup <code> for detailed info.")
        print("-" * 50)
        try:
            while True:
                line = input('cj> ').strip()
                if not line:
                    continue
                if line.lower() in ('exit', 'quit', 'q'):
                    break
                if line.startswith('/lookup '):
                    code = line.split(maxsplit=1)[1].strip()
                    print(show_code_detail(code, code_to_chars))
                    continue
                if line.startswith('/'):
                    print(f"Unknown command: {line}")
                    continue
                decoded, errors = decode_sentence(line, code_to_chars)
                print(decoded)
                if errors:
                    for err in errors:
                        print(f"  {err}", file=sys.stderr)
        except (EOFError, KeyboardInterrupt):
            print()
        return 0

    # Normal decoding mode: from args or stdin
    if args.input:
        raw = ' '.join(args.input)
    else:
        raw = sys.stdin.read().strip()

    if not raw:
        parser.print_help()
        return 1

    decoded, errors = decode_sentence(raw, code_to_chars)
    print(decoded)

    if errors and args.verbose:
        print("\n⚠️  Warnings:", file=sys.stderr)
        for err in errors:
            print(f"  {err}", file=sys.stderr)

    return 0


if __name__ == '__main__':
    sys.exit(main())
