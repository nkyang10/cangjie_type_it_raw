<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/nkyang10/cangjie_type_it_raw/main/.github/banner-dark.svg">
    <img src="https://raw.githubusercontent.com/nkyang10/cangjie_type_it_raw/main/.github/banner-light.svg" alt="Cangjie Type It Raw" width="600">
  </picture>
</p>

<p align="center">
  <strong>倉頡碼解碼器</strong><br>
  將倉頡輸入法編碼解碼為中文字。<br>
  <em>老是忘記切換輸入法？Raw code 照打，我幫你解。</em>
</p>

<p align="center">
  <a href="https://github.com/nkyang10/cangjie_type_it_raw/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-≥3.8-green.svg" alt="Python ≥3.8"></a>
  <a href="https://github.com/nkyang10/cangjie_type_it_raw/actions"><img src="https://github.com/nkyang10/cangjie_type_it_raw/actions/workflows/ci.yml/badge.svg" alt="CI Status"></a>
  <a href="https://github.com/nkyang10/cangjie_type_it_raw/releases"><img src="https://img.shields.io/github/v/release/nkyang10/cangjie_type_it_raw" alt="Latest Release"></a>
</p>

---

## 簡介

**Cangjie Type It Raw** 是一個倉頡輸入法碼解碼器。當你收到一串倉頡編碼（或自己不小心打了 raw code），它會幫你解回正常中文字。

支援混合輸入 — 英文、數字、標點符號會原樣保留，只有倉頡碼會被解碼。還有模糊配對功能，打錯字也找得到。

適合：
- 🤖 **AI agent** — 收到使用者的倉頡編碼訊息，自動解碼再處理
- ⌨️ **使用者** — 常常忘記切換輸入法，打完才發現是 raw code
- 📚 **學習者** — 研究倉頡拆字規則
- 🔧 **開發者** — 整合倉頡解碼功能

## 快速開始

```bash
# 安裝
pip install cangjie-type-it-raw

# 經典案例：又忘記切輸入法了
cj-decode onf okr rmmr okr oin a rtq mk onfd
# → 你知唔知今日咩天氣
# （還要先開天氣 app 確認才回覆）
```

### 🎬 生活情境

#### 「我真的有切換輸入法啦 🤡」

群組裡收到這段訊息，不用叫對方重打，一行指令直接解碼：

```bash
echo "onf kb bucnh owjr omwc rtq hqbu egi ?" | cj-decode
# → 你有睇個價咩看法？
# （還是又賠錢了）
```

#### 凌晨三點 Code 到失智

寫 code 寫到瘋掉，在 Telegram 打了一串倉頡碼當中文發出去。不用刪，解就對了：

```bash
cj-decode onf oin a rtq mk onfd hghu
# → 你今日咩天氣先
# （寫 code 寫到失智還在擔心明天會不會下雨）
```

#### 約喝茶 🥟

一群朋友約吃飯，手機鍵盤又秀逗：

```bash
cj-decode onf oin anau hoami rmmr hoami anb oino tod
# → 你今晚得唔得閒飲茶
# （晚上喝茶？晚上喝茶！港式飲茶萬歲）
```

#### Tech Support Mode 🛠️

朋友：「我打了東西結果都亂碼」

你，進入全 CLI 模式：

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
# 救世主模式。收工。
```

#### 排隊買珍珠奶茶 🧋

排隊中，手機鍵盤鬼打牆，但還是要點飲料：

```bash
cj-decode onf dup oino rtq ? vnhs tod jmyo rksr rlmy
# → 你想飲咩？奶茶定咖啡？
# （珍珠奶茶，永遠的選擇）
```

### 不安裝直接使用

```bash
python3 cj_decoder.py onf okr rmmr okr oin a rtq mk onfd
```

## 功能特色

### 🎯 智能分詞

混合輸入自動識別，英文、數字、標點保留原樣：

```bash
cj-decode onf kb rtq bucnh egi ?
# → 你有咩看法 ？
```

### 🔍 模糊搜尋

打錯不用怕，自動找到最接近的編碼：

```bash
cj-decode --verbose onf okr rtz
# → 你知日
# ⚠️  `rtz` → fuzzy matched `rtq` (口廿手) ≈ 咩 (score: 0.86)
```

### 🖥️ 互動模式

連續解碼，就像一個即時翻譯器：

```bash
cj-decode --interactive
cj> onf kb mu amazon owjr omwc
你有睇 amazon 個價
```

### 📖 編碼查詢

查看每個碼的拆字、對應漢字、Unicode：

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

只要拿 `cj_decoder.py` 和 `cj3.txt` 兩個檔案就行，Python 3.8+ 即可使用，不需要其他 dependency。

## 字典

這個專案使用的字典是 [Cangjie3-Plus](https://github.com/Arthurmcarthur/Cangjie3-Plus)（MIT 授權），由倉頡社群持續維護的倉頡三代碼表，涵蓋：

- 中日韓統一表意文字（基本至擴展 J 區）
- 超過 116,000 條編碼
- 社群持續更新

詳細出處請見 [THIRD_PARTY_NOTICES.md](./THIRD_PARTY_NOTICES.md)。

使用自訂字典：

```bash
cj-decode --dict /path/to/custom.txt onf okr rmmr
```

## AI Agent 使用指引

這個 repo 專為 AI agent 設計，很容易 parse：

```
必要檔案：cj_decoder.py, cj3.txt
入口點：cj_decoder.py （args 或 stdin）
輸出：純文字解碼結果（無 markdown 包裝）
Exit code：0 = 成功, 1 = 錯誤
```

倉頡字母對應表已經內建在 script 中：

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

請見 [CHANGELOG.md](./CHANGELOG.md)。

## 貢獻

歡迎任何貢獻！請見 [CONTRIBUTING.md](./CONTRIBUTING.md)。

## 授權

這個專案採用 [MIT 授權](./LICENSE)。

字典 `cj3.txt` 來自 [Cangjie3-Plus](https://github.com/Arthurmcarthur/Cangjie3-Plus)（MIT），版權歸朱邦復、倉頡之友·馬來西亞及倉頡三代補完計劃所有。

## 鳴謝

- **朱邦復** — 倉頡輸入法發明人
- **倉頡之友·馬來西亞** — 碼表維護社群
- **Arthurmcarthur / 倉頡三代補完計劃** — 完整的 Cangjie3-Plus 字典
