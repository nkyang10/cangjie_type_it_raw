<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/nkyang10/cangjie_type_it_raw/main/.github/banner-dark.svg">
    <img src="https://raw.githubusercontent.com/nkyang10/cangjie_type_it_raw/main/.github/banner-light.svg" alt="Cangjie Type It Raw" width="600">
  </picture>
</p>

<p align="center">
  <strong>倉頡碼解碼器</strong><br>
  將倉頡輸入法編碼解碼為中文字。<br>
  <em>成日唔記得轉輸入法？Raw code 照打，我幫你解。</em>
</p>

<p align="center">
  <a href="https://github.com/nkyang10/cangjie_type_it_raw/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-≥3.8-green.svg" alt="Python ≥3.8"></a>
  <a href="https://github.com/nkyang10/cangjie_type_it_raw/actions"><img src="https://github.com/nkyang10/cangjie_type_it_raw/actions/workflows/ci.yml/badge.svg" alt="CI Status"></a>
  <a href="https://github.com/nkyang10/cangjie_type_it_raw/releases"><img src="https://img.shields.io/github/v/release/nkyang10/cangjie_type_it_raw" alt="Latest Release"></a>
</p>

---

## 簡介

**Cangjie Type It Raw** 係一個倉頡輸入法碼解碼器。當你收到一串倉頡編碼（或者自己唔小心打咗 raw code），佢會幫你解返做正常中文字。

支援混合輸入 — 英文、數字、標點符號會原樣保留，只有倉頡碼會被解碼。仲有模糊配對功能，打錯字都搵到。

適合：
- 🤖 **AI agent** — 收到 user 嘅倉頡編碼訊息，自動解碼先再處理
- ⌨️ **用家** — 成日唔記得轉輸入法，打完先發現係 raw code
- 📚 **學習者** — 研究倉頡拆字規則
- 🔧 **開發者** — 整合倉頡解碼功能

## 快速開始

```bash
# 安裝
pip install cangjie-type-it-raw

# 解碼一句句子
cj-decode onf okr rmmr okr oin a rtq mk onfd
# → 你知唔知今日咩天氣

# 混合輸入（英文/數字原樣保留）
cj-decode 2 amazon owjr omwc rtq bucnh egi
# → 2 amazon 個價咩看法？

# Pipe 輸入
echo "onf okr rmmr" | cj-decode

# 互動模式
cj-decode --interactive

# 查單一編碼
cj-decode --lookup onf
```

### 唔安裝直接用

```bash
python3 cj_decoder.py onf okr rmmr okr oin a rtq mk onfd
```

## 功能特色

### 🎯 智能分詞

混合輸入自動識別，英文、數字、標點保留原樣：

```bash
cj-decode umr umr smmri anau 2 amazon owjr omwc rtm nmnsm
# → 岩岩尋晚 2 amazon 個價咁驺

cj-decode onf kb rtq bucnh egi ?
# → 你有咩看法 ？
```

### 🔍 模糊搜尋

打錯唔怕，自動搵最接近嘅編碼：

```bash
cj-decode --verbose onf okr rtz
# → 你知日
# ⚠️  `rtz` → fuzzy matched `rtq` (口廿手) ≈ 咩 (score: 0.86)
```

### 🖥️ 互動模式

連續解碼，好似一個即時翻譯器：

```bash
cj-decode --interactive
cj> onf kb mu amazon owjr omwc
你有睇 amazon 個價
```

### 📖 編碼查詢

睇每個碼嘅拆字、對應漢字、Unicode：

```bash
cj-decode --lookup onf
# Code: onf
# Radicals: 人 → 弓 → 火
# Characters (1):
#   1. 你 (U+4F60)
```

## 安裝

### pip（推薦）

```bash
pip install cangjie-type-it-raw
```

### 原始碼安裝

```bash
git clone https://github.com/nkyang10/cangjie_type_it_raw.git
cd cangjie_type_it_raw
pip install -e .
```

### 零安裝（即用版）

就咁拎 `cj_decoder.py` 同 `cj3.txt` 兩個檔案就得，Python 3.8+ 已經夠用，唔使其他 dependency。

## 字典

呢個 project 用嘅字典係 [Cangjie3-Plus](https://github.com/Arthurmcarthur/Cangjie3-Plus)（MIT 授權），由倉頡社群持續維護嘅倉頡三代碼表，覆蓋：

- 中日韓統一表意文字（基本至擴展 J 區）
- 超過 116,000 條編碼
- 社群持續更新

詳細出處請睇 [THIRD_PARTY_NOTICES.md](./THIRD_PARTY_NOTICES.md)。

用自訂字典：

```bash
cj-decode --dict /path/to/custom.txt onf okr rmmr
```

## AI Agent 使用指引

呢個 repo 專為 AI agent 設計，好容易 parse：

```
必要檔案：cj_decoder.py, cj3.txt
入口點：cj_decoder.py （args 或 stdin）
輸出：純文字解碼結果（冇 markdown 包裝）
Exit code：0 = 成功, 1 = 錯誤
```

倉頡字母對應表已經內置喺 script 入面：

| 字母 | 字根 | 類別 | | 字母 | 字根 | 類別 |
|------|------|------|-|------|------|------|
| A | 日 | 哲理類 | | N | 弓 | 筆畫類 |
| B | 月 | 哲理類 | | O | 人 | 人體類 |
| C | 金 | 哲理類 | | P | 心 | 人體類 |
| D | 木 | 哲理類 | | Q | 手 | 人體類 |
| E | 水 | 哲理類 | | R | 口 | 人體類 |
| F | 火 | 哲理類 | | S | 尸 | 字型類 |
| G | 土 | 哲理類 | | T | 廿 | 字型類 |
| H | 竹 | 筆畫類 | | U | 山 | 字型類 |
| I | 戈 | 筆畫類 | | V | 女 | 字型類 |
| J | 十 | 筆畫類 | | W | 田 | 字型類 |
| K | 大 | 筆畫類 | | X | 難 | 難字 |
| L | 中 | 筆畫類 | | Y | 卜 | 字型類 |
| M | 一 | 筆畫類 | | Z | (重) | 重覆鍵 |

## API 整合（Python）

```python
import subprocess

def decode_cangjie(text: str) -> str:
    result = subprocess.run(
        ['cj-decode'], input=text, capture_output=True, text=True
    )
    return result.stdout.strip()
```

## 更新記錄

請睇 [CHANGELOG.md](./CHANGELOG.md)。

## 貢獻

歡迎任何貢獻！請睇 [CONTRIBUTING.md](./CONTRIBUTING.md)。

## 授權

呢個 project 係 [MIT 授權](./LICENSE)。

字典 `cj3.txt` 來自 [Cangjie3-Plus](https://github.com/Arthurmcarthur/Cangjie3-Plus)（MIT），版權歸朱邦復、倉頡之友·馬來西亞及倉頡三代補完計劃所有。

## 鳴謝

- **朱邦復** — 倉頡輸入法發明人
- **倉頡之友·馬來西亞** — 碼表維護社群
- **Arthurmcarthur / 倉頡三代補完計劃** — 完整嘅 Cangjie3-Plus 字典
