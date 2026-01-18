# GitHubリポジトリ作成手順

## ⚠️ 重要: まずGitHubでリポジトリを作成してください

リポジトリがまだ存在しないため、以下の手順で作成してください。

## Step 1: GitHubでリポジトリを作成

1. **GitHubにログイン**: https://github.com/login
2. **新しいリポジトリを作成**: https://github.com/new
3. **リポジトリ情報を入力**:
   - **Repository name**: `shap-stability-analysis`
   - **Description**: `Stability and Faithfulness Analysis of SHAP Explanations for Tabular Machine Learning Models`
   - **Visibility**: Public または Private（お好みで）
   - ⚠️ **重要**: README、.gitignore、LICENSEは**追加しない**（既にローカルにあります）
4. **"Create repository"をクリック**

## Step 2: ローカルでGitを設定

リポジトリを作成したら、以下のコマンドを実行：

```powershell
cd C:\Users\nishi\Life\iML_Project_Stability_Analysis

# 既存のリモートを削除（エラーが出た場合）
git remote remove origin

# 新しいリモートを追加
git remote add origin https://github.com/keisuke58/shap-stability-analysis.git

# リモートを確認
git remote -v

# メインブランチに切り替え
git branch -M main

# コードをプッシュ
git push -u origin main
```

## Step 3: 認証

初回プッシュ時、GitHubの認証が必要です：
- Personal Access Token (PAT) を使用
- または GitHub CLI (`gh auth login`)

## トラブルシューティング

### エラー: "remote origin already exists"
```powershell
git remote remove origin
git remote add origin https://github.com/keisuke58/shap-stability-analysis.git
```

### エラー: "Repository not found"
- GitHubでリポジトリが作成されているか確認
- リポジトリ名が正確か確認: `shap-stability-analysis`
- ユーザー名が正確か確認: `keisuke58`

### 認証エラー
Personal Access Tokenを作成:
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. "Generate new token" → 必要な権限を選択（repo）
3. トークンをコピーして使用

## 完了後

リポジトリが正常にプッシュされたら：
- https://github.com/keisuke58/shap-stability-analysis で確認できます
- PDFはGitHub Releasesに追加することを推奨
