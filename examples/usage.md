# Cangjie Type It Raw — Usage Examples

## Basic Commands

```bash
# Decode a full sentence
cj-decode onf okr rmmr okr oin a rtq mk onfd
# → 你知唔知今日咩天氣

# Mixed with English and numbers
cj-decode onf kb mu 2 amazon owjr omwc rtq bucnh
# → 你有睇 2 amazon 個價咩看法

# Mixed with question
cj-decode onf okr rmmr okr oin a rtq mk onfd ?
# → 你知唔知今日咩天氣 ？
```

## Learning Cangjie Composition

Use `--lookup` to see how characters are composed:

```bash
# 你 = 人(on) + 弓(n) + 火(f)
cj-decode --lookup onf
```

## Typo Correction

Compare exact vs fuzzy:

```bash
# Exact decode
cj-decode onf okr rtq
# → 你知咩

# With typo (rtz instead of rtq)
cj-decode --verbose onf okr rtz
# → 你知咩
# ⚠️  `rtz` → fuzzy matched `rtq` (口廿手) ≈ 咩 (score: 0.86)
```

## Interactive Session

```bash
cj-decode --interactive
cj> onf kb mu amazon owjr omwc
你有睇 amazon 個價
cj> /lookup okr
Code: okr
Radicals: 人 → 大 → 口
Characters (1):
  1. 知 (U+77E5)
cj> exit
```

## Using as a Python Library

```python
from cj_decoder import load_dictionary, decode_sentence

code_to_chars, _ = load_dictionary('cj3.txt')
decoded, errors = decode_sentence('onf okr rmmr', code_to_chars)
print(decoded)  # 你知唔
```

## Using with xclip (Linux)

```bash
# Decode clipboard content
xclip -o -selection clipboard | cj-decode | xclip -selection clipboard
```

## Decoding from a File

```bash
cat cangjie_messages.txt | cj-decode > decoded.txt
```
