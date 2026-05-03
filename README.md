# python-automation

Playwright を使った Web スクレイピング自動化プロジェクト。

## 機能

- JavaScript レンダリングページからのデータ取得（Playwright 使用）
- robots.txt を確認してから対象 URL にアクセス
- リクエスト間に 1〜3 秒のランダム待機
- 結果を Markdown ファイルとスクリーンショットとして保存

## 必要環境

- Python 3.11 以上
- Git

## セットアップ

```powershell
# リポジトリをクローン
git clone https://github.com/ShinCom1974/python-automation.git
cd python-automation

# 仮想環境を作成・有効化
python -m venv .venv
.venv\Scripts\Activate.ps1

# 依存パッケージをインストール
pip install -r requirements.txt

# Playwright ブラウザ（Chromium）をインストール
playwright install chromium
```

## スクリプト一覧

### `scripts/quotes_scraper.py`

[quotes.toscrape.com/js](https://quotes.toscrape.com/js) から名言と著者名を取得するスクレイパー。

**実行方法：**

```powershell
# 仮想環境を有効化してから実行
python scripts/quotes_scraper.py

# または仮想環境を有効化せず直接実行
.venv\Scripts\python.exe scripts/quotes_scraper.py
```

**出力ファイル：**

| ファイル名 | 内容 |
|---|---|
| `quotes_YYYYMMDD.md` | 取得した名言・著者名を Markdown 形式でまとめたもの |
| `quotes_YYYYMMDD.png` | 実行時のページ全体スクリーンショット |
| `scraper.log` | 実行ログ（.gitignore 対象） |

## 依存パッケージ

```
requests==2.31.0
beautifulsoup4==4.12.3
playwright==1.49.0
```
