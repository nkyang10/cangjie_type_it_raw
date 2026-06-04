"""Tests for the Cangjie decoder."""

import sys
import os
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from cj_decoder import (
    is_cangjie_code,
    is_likely_english,
    tokenize,
    load_dictionary,
    decode_cangjie,
    decode_sentence,
    fuzzy_search,
    CANGJIE_MAP,
)


def _get_dict():
    dict_path = os.path.join(os.path.dirname(__file__), '..', 'cj3.txt')
    code_to_chars, char_to_codes = load_dictionary(dict_path)
    return code_to_chars, char_to_codes


# ── Cangjie map ────────────────────────────────────────────────────────

class TestCangjieMap:
    def test_has_all_letters(self):
        assert len(CANGJIE_MAP) == 26

    def test_specific_mappings(self):
        assert CANGJIE_MAP['a'] == '日'
        assert CANGJIE_MAP['b'] == '月'
        assert CANGJIE_MAP['x'] == '難'


# ── Token classification ──────────────────────────────────────────────

class TestIsCangjieCode:
    def test_valid_codes(self):
        assert is_cangjie_code('onf')
        assert is_cangjie_code('okr')
        assert is_cangjie_code('rmmr')
        assert is_cangjie_code('a')  # Single letter is valid Cangjie
        assert is_cangjie_code('rtq')

    def test_common_english_not_cangjie(self):
        assert not is_cangjie_code('amazon')
        assert not is_cangjie_code('google')
        assert not is_cangjie_code('apple')
        assert not is_cangjie_code('the')
        assert not is_cangjie_code('this')

    def test_too_long(self):
        assert not is_cangjie_code('abcdef')
        assert not is_cangjie_code('onfabc')

    def test_non_alpha(self):
        assert not is_cangjie_code('onf1')
        assert not is_cangjie_code('onf.')

    def test_uppercase(self):
        assert not is_cangjie_code('ONF')
        assert not is_cangjie_code('Onf')


class TestIsLikelyEnglish:
    def test_common_words(self):
        assert is_likely_english('the')
        assert is_likely_english('this')
        assert is_likely_english('that')
        assert is_likely_english('amazon')
        assert is_likely_english('google')

    def test_short_codes_not_english(self):
        assert not is_likely_english('onf')
        assert not is_likely_english('okr')
        assert not is_likely_english('rtq')


class TestTokenizer:
    def test_pure_cangjie(self):
        tokens = tokenize('onf okr rmmr')
        types = [t[0] for t in tokens]
        assert types == ['cangjie', 'cangjie', 'cangjie']

    def test_mixed_input(self):
        tokens = tokenize('onf kb mu amazon owjr omwc')
        types = [t[0] for t in tokens]
        assert types == ['cangjie', 'cangjie', 'cangjie', 'literal', 'cangjie', 'cangjie']

    def test_numbers_passthrough(self):
        tokens = tokenize('onf 2 okr')
        assert tokens[1] == ('number', '2')

    def test_punctuation_passthrough(self):
        tokens = tokenize('onf ? okr')
        assert tokens[1] == ('punct', '?')

    def test_ambiguous_context(self):
        """Short ambigous words between Cangjie codes should be reclassified."""
        tokens = tokenize('onf okr a onfd')
        assert tokens[2] == ('cangjie', 'a')


# ── Decoding ──────────────────────────────────────────────────────────

class TestDecoding:
    def test_basic_decode(self):
        code_to_chars, _ = _get_dict()
        result, errors = decode_sentence('onf okr rmmr', code_to_chars)
        assert result == '你知唔'
        assert errors == []

    def test_full_sentence(self):
        code_to_chars, _ = _get_dict()
        result, errors = decode_sentence('onf okr rmmr okr oin a rtq mk onfd', code_to_chars)
        assert result == '你知唔知今日咩天氣'
        assert errors == []

    def test_mixed_decode(self):
        code_to_chars, _ = _get_dict()
        result, errors = decode_sentence('onf kb bucnh amazon owjr omwc', code_to_chars)
        assert '你' in result
        assert '有' in result
        assert '睇' in result
        assert 'amazon' in result
        assert '個' in result
        assert '價' in result

    def test_decode_single(self):
        code_to_chars, _ = _get_dict()
        decoded, errors, _ = decode_cangjie(['onf'], code_to_chars)
        assert decoded == '你'

    def test_decode_multiple_with_mixed(self):
        code_to_chars, _ = _get_dict()
        decoded, errors, fuzzy = decode_cangjie(['onf', 'okr'], code_to_chars)
        assert decoded == '你知'
        assert errors == []

    def test_cangjie_map_integrity(self):
        """Test that Cangjie codes decode to Chinese, not to ASCII."""
        code_to_chars, _ = _get_dict()
        result, errors = decode_sentence('onf okr rmmr okr oin a rtq mk onfd', code_to_chars)
        assert all('\u4e00' <= c <= '\u9fff' or c == ' ' for c in result), \
            f"Output contains non-CJK chars: {result}"

    def test_mixed_with_correct_look(self):
        """睇 = bucnh in Cangjie 3"""
        code_to_chars, _ = _get_dict()
        result, errors = decode_sentence('onf kb bucnh amazon owjr omwc', code_to_chars)
        assert '你' in result
        assert '有' in result
        assert '睇' in result
        assert 'amazon' in result
        assert '個' in result
        assert '價' in result


# ── Fuzzy matching ────────────────────────────────────────────────────

class TestFuzzyMatching:
    def test_fuzzy_corrects_typo(self):
        code_to_chars, _ = _get_dict()
        # rtz is a typo for rtq (咩)
        candidates = fuzzy_search('rtz', code_to_chars)
        assert len(candidates) > 0
        # Should find rtq
        codes_found = [c[1] for c in candidates]
        assert 'rtq' in codes_found

    def test_fuzzy_empty_input(self):
        code_to_chars, _ = _get_dict()
        candidates = fuzzy_search('zzzzz', code_to_chars)
        assert len(candidates) == 0


# ── Dictionary ────────────────────────────────────────────────────────

class TestDictionary:
    def test_dict_loaded(self):
        code_to_chars, char_to_codes = _get_dict()
        assert len(code_to_chars) > 50000  # Should have 50k+ codes

    def test_known_codes(self):
        code_to_chars, _ = _get_dict()
        assert 'onf' in code_to_chars  # 你
        assert 'okr' in code_to_chars  # 知
        assert 'rmmr' in code_to_chars  # 唔
        assert 'oin' in code_to_chars  # 今
        assert 'a' in code_to_chars  # 日
        assert 'rtq' in code_to_chars  # 咩
        assert 'mk' in code_to_chars  # 天
        assert 'onfd' in code_to_chars  # 氣
