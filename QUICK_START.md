# クイックスタートガイド

## 🚀 5分で始める

### 1. 環境セットアップ（1分）

```bash
# プロジェクトフォルダに移動
cd C:\Users\nishi\Life\iML_Project_Stability_Analysis

# 仮想環境作成（推奨）
python -m venv venv
venv\Scripts\activate

# 依存パッケージインストール
pip install -r requirements.txt
```

### 2. データ準備（1分）

Jupyter Notebookを開いて実行：
```bash
jupyter notebook notebooks/01_data_preprocessing.ipynb
```

または、Pythonスクリプトで実行：
```bash
python -c "from src.data_loader import load_adult_income, prepare_data; X, y = load_adult_income(); X_train, X_test, y_train, y_test, _ = prepare_data(X, y); print('Data ready!')"
```

### 3. モデル訓練（2分）

```bash
jupyter notebook notebooks/02_model_training.ipynb
```

### 4. SHAP説明生成（5-10分）

```bash
jupyter notebook notebooks/03_shap_explanations.ipynb
```

**注意**: KernelSHAPは時間がかかります。最初は5シード程度で実行してください。

### 5. 安定性分析（1分）

```bash
jupyter notebook notebooks/04_stability_analysis.ipynb
```

### 6. 可視化（1分）

```bash
jupyter notebook notebooks/05_visualization.ipynb
```

---

## 🎯 または、一括実行

```bash
python run_full_pipeline.py
```

これで全てのステップが自動実行されます（約20-30分かかります）。

---

## 📊 どこまでやればいいか

### 最低限（合格レベル）
- ✅ データセット1つ
- ✅ モデル3つ（各5-10シード）
- ✅ SHAP説明生成
- ✅ 安定性分析（XGBoostのみでOK）
- ✅ 基本的な可視化（5-7個の図表）

**時間**: 約15-20時間

### 推奨（良い成績）
- 上記 + 全モデルでの分析 + データサブサンプリング分析

**時間**: 約25-30時間

---

詳細は `WHAT_TO_IMPLEMENT.md` を参照してください。
