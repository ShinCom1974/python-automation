# CLAUDE.md

## プロジェクト概要

Python自動化スクリプト群のプロジェクト。

## 開発環境

- 言語: Python 3.x
- OS: Windows 11
- パッケージ管理: pip / requirements.txt

## Git運用ルール

**コードを変更するたびに、必ずGitHubにプッシュすること。**

### 手順

1. 変更をステージング
   ```
   git add <変更ファイル>
   ```
2. コミット（変更内容を日本語または英語で簡潔に記述）
   ```
   git commit -m "変更内容の説明"
   ```
3. GitHubへプッシュ
   ```
   git push origin main
   ```

### コミットメッセージ規則

- 新機能追加: `feat: 説明`
- バグ修正: `fix: 説明`
- リファクタリング: `refactor: 説明`
- ドキュメント: `docs: 説明`
- その他: `chore: 説明`

### 注意事項

- `.env` ファイルや認証情報は絶対にコミットしない
- `git push --force` は使用しない
- コードを変更・追加したら、その都度プッシュする（まとめてのプッシュは避ける）

## コーディング規約

- PEP 8 に準拠
- 関数・変数名はスネークケース（`snake_case`）
- クラス名はパスカルケース（`PascalCase`）
- コメントは必要最小限（コードが自己説明的になるよう命名で対応）

## ファイル構成（想定）

```
python-automation/
├── CLAUDE.md
├── requirements.txt
├── .gitignore
└── scripts/        # 自動化スクリプト
```
