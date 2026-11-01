# e-sign Calendar Converter

e-paper ディスプレイ向けの画像変換ツールです。PNG または SVG を
400 x 300 ピクセル、黒・白・赤・黄の4色画像に変換します。

## 動作環境

- Python 3.10 以上

## セットアップ

必要なパッケージをインストールします。

```powershell
python -m pip install -r requirements.txt
```

## 使い方

引数を指定せずに実行すると、`cal.png` を `cal_epaper.png` に変換します。

```powershell
python convert_epaper.py
```

入力ファイルを指定する場合は、引数にファイルパスを指定します。

```powershell
python convert_epaper.py cal.svg
python convert_epaper.py cal.png output.png
```

### 引数

| 引数 | 説明 |
| --- | --- |
| `source` | 入力する PNG または SVG（省略時は `cal.png`） |
| `output` | 出力先 PNG（省略時は入力ファイル名に `_epaper.png` を付けた名前） |

## 出力色

変換後の画像は次の4色に量子化されます。

- 黒: `(0, 0, 0)`
- 白: `(255, 255, 255)`
- 赤: `(255, 0, 0)`
- 黄: `(255, 255, 0)`
