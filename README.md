<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/nkyang10/cangjie_type_it_raw/main/.github/banner-dark.svg">
    <img src="https://raw.githubusercontent.com/nkyang10/cangjie_type_it_raw/main/.github/banner-light.svg" alt="Cangjie Type It Raw" width="600">
  </picture>
</p>

<p align="center">
  <strong>倉頡碼解碼器 — Cangjie Input Code Decoder</strong><br>
  Turn Cangjie key sequences into Chinese characters.
  <em>Because sometimes you just type raw codes and need a decoder.</em>
</p>

<p align="center">
  <a href="https://github.com/nkyang10/cangjie_type_it_raw/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-≥3.8-green.svg" alt="Python ≥3.8"></a>
  <a href="https://github.com/nkyang10/cangjie_type_it_raw/actions"><img src="https://github.com/nkyang10/cangjie_type_it_raw/actions/workflows/ci.yml/badge.svg" alt="CI Status"></a>
  <a href="https://github.com/nkyang10/cangjie_type_it_raw/releases"><img src="https://img.shields.io/github/v/release/nkyang10/cangjie_type_it_raw" alt="Latest Release"></a>
  <a href="https://github.com/Arthurmcarthur/Cangjie3-Plus"><img src="https://img.shields.io/badge/dictionary-Cangjie3--Plus-4ea94b" alt="Dictionary: Cangjie3-Plus"></a>
</p>

---

> 🌐 **中文版：[香港粵語](README.zh-HK.md) · [台灣繁體](README.zh-TW.md)**

---

## Overview

**Cangjie Type It Raw** decodes Cangjie input method (倉頡輸入法) key sequences into Chinese characters. It handles mixed input — English words, numbers, and punctuation pass through unchanged while Cangjie codes are decoded in context. Fuzzy matching automatically corrects typos.

Perfect for:
- 🤖 **AI agents** that receive Cangjie-encoded text and need to display it as Chinese
- ⌨️ **Typists** who forget to switch input modes and end up with raw codes
- 📚 **Learners** studying Cangjie composition
- 🔧 **Developers** integrating Cangjie decoding into their tools

## Quick Start

```bash
# Install
pip install cangjie-type-it-raw

# The classic: "Ah crap, I typed in Cangjie again"
cj-decode onf okr rmmr okr oin a rtq mk onfd
# → 你知唔知今日咩天氣
# (Translation: "Do you know what the weather's like today?")
```

### 🎬 Real-Life Scenarios

#### "Bro I swear I switched to Chinese"

Your friend just sent you this in a group chat. Don't make them retype it — decode it in one line.

```bash
echo "onf kb bucnh owjr omwc rtq hqbu egi ?" | cj-decode
# → 你有睇個價咩看法？
# ("Did you see the price? What do you think?")
```

#### 3AM Coding Sprint

You're deep in a terminal, half-asleep, and accidentally typed Cangjie codes straight into your Telegram message instead of Chinese. Don't delete it — decode it.

```bash
cj-decode onf oin a rtq mk onfd hghu
# → 你今日咩天氣先
# Because even sleep-deprived, you're still asking about the weather.
```

#### Dim Sum Run 🥟

Planning a chaotic dim sum trip with friends:

```bash
cj-decode onf oin anau hoami rmmr hoami anb oino tod
# → 你今晚得唔得閒飲茶
# ("You free tonight for dim sum?")
```

#### Tech-Support Mode 🛠️

Your friend: "I typed something in and it came out all weird"

You, in full CLI energy:

```bash
cj-decode --interactive
cj> onf okr rmmr okr onfd
你知唔知氣
cj> /lookup onfd
Code: onfd
Radicals: 人 → 弓 → 火 → 木
Characters (1):
  1. 氣 (U+6C23)
cj> ^D
# Problem solved. You're a hero.
```

#### Bubble Tea Line 🧋

Standing in line, phone keyboard glitching, still need to order:

```bash
cj-decode onf dup oino rtq ? vnhs tod jmyo rksr rlmy
# → 你想飲咩？奶茶定咖啡？
# (Bubble tea or coffee? The eternal debate.)
```

### Run Without Installing

```bash
python3 cj_decoder.py onf okr rmmr okr oin a rtq mk onfd
```

## Features

### 🎯 Smart Tokenization

Mixed input is handled seamlessly — English words, numbers, and punctuation are left as-is while Cangjie codes are decoded:

```bash
cj-decode onf kb rtq bucnh egi ?
# → 你有咩看法 ？
```

### 🔍 Fuzzy Typo Correction

Missed a key? No problem. The decoder finds the closest matching code:

```bash
cj-decode --verbose onf okr rtz
# → 你知日
# ⚠️  `rtz` → fuzzy matched `rtq` (口廿手) ≈ 咩 (score: 0.86)
```

### 🖥️ Interactive Mode

Start a live session for continuous decoding:

```bash
cj-decode --interactive
```

### 📖 Code Lookup

Inspect the radicals, character mappings, and Unicode codepoints for any Cangjie code:

```bash
cj-decode --lookup onf
# Code: onf
# Radicals: 人 → 弓 → 火
# Characters (1):
#   1. 你 (U+4F60)
```

## Installation

### pip (recommended)

```bash
pip install cangjie-type-it-raw
```

### From source

```bash
git clone https://github.com/nkyang10/cangjie_type_it_raw.git
cd cangjie_type_it_raw
pip install -e .
```

### Zero-install (standalone script)

Just copy `cj_decoder.py` and `cj3.txt` anywhere — they work together with no dependencies beyond Python 3.8+.

## Dictionary

The bundled dictionary (`cj3.txt`) is the [Cangjie3-Plus](https://github.com/Arthurmcarthur/Cangjie3-Plus) project — an MIT-licensed, community-maintained Cangjie 3rd generation code table covering:

- CJK Unified Ideographs (Basic to Extension J)
- 116,000+ entries
- Continuously updated by the Cangjie community

See [THIRD_PARTY_NOTICES.md](./THIRD_PARTY_NOTICES.md) for attribution.

To use a custom dictionary:

```bash
cj-decode --dict /path/to/your/cj3.txt onf okr rmmr
```

## Version History

See [CHANGELOG.md](./CHANGELOG.md).

## For AI Agents

This repo is designed to be easily parsed and used by AI coding agents:

```
Context files needed: cj_decoder.py, cj3.txt
Entry point: cj_decoder.py accepts args or stdin
Output: decoded Chinese text (unambiguous, no markdown wrapping)
Exit code: 0 on success, 1 on error
```

The Cangjie letter-to-radical mapping is embedded in the script itself:

| Letter | Radical | Category | | Letter | Radical | Category |
|--------|---------|----------|-|--------|---------|----------|
| A | 日 | Philosophy | | N | 弓 | Stroke |
| B | 月 | Philosophy | | O | 人 | Body |
| C | 金 | Philosophy | | P | 心 | Body |
| D | 木 | Philosophy | | Q | 手 | Body |
| E | 水 | Philosophy | | R | 口 | Body |
| F | 火 | Philosophy | | S | 尸 | Shape |
| G | 土 | Philosophy | | T | 廿 | Shape |
| H | 竹 | Stroke | | U | 山 | Shape |
| I | 戈 | Stroke | | V | 女 | Shape |
| J | 十 | Stroke | | W | 田 | Shape |
| K | 大 | Stroke | | X | 難 | Difficult |
| L | 中 | Stroke | | Y | 卜 | Shape |
| M | 一 | Stroke | | Z | (repeat) | Repeat |

## Use Cases

### AI / LLM Integration

When an LLM receives raw Cangjie codes in user input (common on mobile/keyboard platforms), use this tool to transparently decode before processing:

```python
import subprocess

def decode_cangjie(text: str) -> str:
    result = subprocess.run(
        ['cj-decode'], input=text, capture_output=True, text=True
    )
    return result.stdout.strip()
```

### Keyboard Macro / Snippet

Bind to a hotkey to decode the current clipboard content:

```bash
pbpaste | cj-decode | pbcopy   # macOS
xclip -o | cj-decode | xclip   # Linux
```

## Contributing

Contributions welcome! See [CONTRIBUTING.md](./CONTRIBUTING.md).

## License

This project is [MIT licensed](./LICENSE).

The bundled dictionary `cj3.txt` is from [Cangjie3-Plus](https://github.com/Arthurmcarthur/Cangjie3-Plus) (MIT), copyright 朱邦復, 倉頡之友·馬來西亞, and 倉頡三代補完計劃.

## Acknowledgments

- **朱邦復** (Chu Bong-Foo) — Inventor of the Cangjie input method
- **倉頡之友·馬來西亞** — Cangjie user community maintaining and revising the code tables
- **Arthurmcarthur** / **倉頡三代補完計劃** — The comprehensive Cangjie3-Plus dictionary
