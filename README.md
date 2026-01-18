# SHAP Stability Analysis Project

**Project Title**: Stability and Faithfulness Analysis of SHAP Explanations for Tabular Models  
**Course**: Interpretierbares Maschinelles Lernen (Interpretable Machine Learning)  
**Student**: Keisuke Nishioka (Matrikelnummer: 10081049)  
**Instructor**: Prof. Dr. rer. nat. Marius Lindauer

---

## 📋 プロジェクト概要 / Project Overview

このプロジェクトでは、SHAP説明の安定性と信頼性を分析します。異なるランダムシード、データサブサンプリング、モデルクラスにおけるSHAP説明の一貫性を評価します。

This project analyzes the stability and faithfulness of SHAP explanations. We evaluate the consistency of SHAP explanations across different random seeds, data subsampling, and model classes.

---

## 🎯 実装範囲 / Implementation Scope

### ✅ 実装すべき内容 / What to Implement

#### Phase 1: データ準備とモデル訓練 / Data Preparation and Model Training
- [x] データセットの選択と読み込み / Dataset selection and loading
- [x] データ前処理（欠損値処理、エンコーディング） / Data preprocessing (missing value handling, encoding)
- [x] 3つのモデルの実装と訓練 / Implementation and training of 3 models
  - XGBoost (TreeSHAP)
  - Random Forest (TreeSHAP)
  - Logistic Regression (KernelSHAP)

#### Phase 2: SHAP説明の生成 / SHAP Explanation Generation
- [x] TreeSHAPの実装（XGBoost, Random Forest用） / TreeSHAP implementation (for XGBoost, Random Forest)
- [x] KernelSHAPの実装（Logistic Regression用） / KernelSHAP implementation (for Logistic Regression)
- [x] 複数のランダムシードでの説明生成 / Explanation generation with multiple random seeds
- [x] 異なるデータサブサンプリング率での説明生成 / Explanation generation with different data subsampling rates

#### Phase 3: 安定性分析 / Stability Analysis
- [x] Feature Ranking Correlation（Spearman相関）の計算 / Feature Ranking Correlation (Spearman correlation) calculation
- [x] SHAP Value Varianceの計算 / SHAP Value Variance calculation
- [x] Explanation Consistency（top-k特徴量の一貫性）の計算 / Explanation Consistency (top-k feature consistency) calculation
- [x] モデル間比較 / Model comparison
- [x] サンプルサイズ効果の分析 / Sample size effect analysis

#### Phase 4: 可視化 / Visualization
- [x] SHAP summary plots
- [x] Feature ranking correlation heatmaps
- [x] SHAP value variance box plots
- [x] Stability comparison across models
- [x] Sample size effect visualizations

#### Phase 5: 結果のまとめ / Results Summary
- [x] 安定性条件の特定 / Identification of stability conditions
- [x] 実用的な推奨事項の整理 / Organization of practical recommendations
- [x] 結果の解釈と考察 / Interpretation and discussion of results

### ❌ 実装しない内容（スコープ外） / Out of Scope

- 新規アルゴリズムの開発 / Development of new algorithms
- LIMEや他の手法との比較 / Comparison with LIME and other methods
- 画像・テキストデータの処理 / Image and text data processing
- 高計算コストモデル（Deep Learning等） / High computational cost models (Deep Learning, etc.)

---

## 📁 プロジェクト構造 / Project Structure

```
iML_Project_Stability_Analysis/
├── README.md                          # このファイル / This file
├── requirements.txt                   # Python依存パッケージ / Python dependencies
├── config.py                          # 設定ファイル（random seeds, データセット等） / Configuration file (random seeds, datasets, etc.)
│
├── data/                              # データセット / Datasets
│   ├── raw/                           # 生データ / Raw data
│   └── processed/                      # 前処理済みデータ / Processed data
│
├── notebooks/                         # Jupyter Notebooks
│   ├── 01_data_preprocessing.ipynb    # データ前処理 / Data preprocessing
│   ├── 02_model_training.ipynb       # モデル訓練 / Model training
│   ├── 03_shap_explanations.ipynb    # SHAP説明生成 / SHAP explanation generation
│   ├── 04_stability_analysis.ipynb   # 安定性分析 / Stability analysis
│   └── 05_visualization.ipynb        # 可視化 / Visualization
│
├── src/                               # Pythonモジュール / Python modules
│   ├── __init__.py
│   ├── data_loader.py                 # データ読み込み / Data loading
│   ├── models.py                      # モデル定義と訓練 / Model definition and training
│   ├── shap_analysis.py              # SHAP説明生成 / SHAP explanation generation
│   ├── stability_metrics.py           # 安定性指標の計算 / Stability metrics calculation
│   └── visualization.py              # 可視化関数 / Visualization functions
│
├── results/                           # 結果ファイル / Results
│   ├── figures/                       # 図表（PNG/PDF） / Figures (PNG/PDF)
│   ├── tables/                        # 表（CSV） / Tables (CSV)
│   └── shap_values/                  # 保存されたSHAP値（NPZ） / Saved SHAP values (NPZ)
│
├── final_report.tex                   # 最終レポート（LaTeX） / Final report (LaTeX)
├── poster.tex                         # ポスター（LaTeX） / Poster (LaTeX)
│
└── .gitignore                         # Git除外ファイル / Git ignore file
```

---

## 🚀 実装の進め方 / How to Run

### Step 1: 環境セットアップ / Environment Setup
```bash
# 仮想環境作成（推奨） / Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 依存パッケージインストール / Install dependencies
pip install -r requirements.txt
```

### Step 2: データ準備 / Data Preparation
- `notebooks/01_data_preprocessing.ipynb` を実行 / Run `notebooks/01_data_preprocessing.ipynb`
- データセットを `data/raw/` に配置 / Place datasets in `data/raw/`

### Step 3: モデル訓練 / Model Training
- `notebooks/02_model_training.ipynb` を実行 / Run `notebooks/02_model_training.ipynb`
- 複数のランダムシードで訓練 / Train with multiple random seeds

### Step 4: SHAP説明生成 / SHAP Explanation Generation
- `notebooks/03_shap_explanations.ipynb` を実行 / Run `notebooks/03_shap_explanations.ipynb`
- TreeSHAPとKernelSHAPの両方を実装 / Implement both TreeSHAP and KernelSHAP

### Step 5: 安定性分析 / Stability Analysis
- `notebooks/04_stability_analysis.ipynb` を実行 / Run `notebooks/04_stability_analysis.ipynb`
- 評価指標を計算 / Calculate evaluation metrics

### Step 6: 可視化 / Visualization
- `notebooks/05_visualization.ipynb` を実行 / Run `notebooks/05_visualization.ipynb`
- 結果を `results/figures/` に保存 / Save results to `results/figures/`

### Step 7: レポートとポスターの生成 / Generate Report and Poster
```bash
# LaTeXファイルをコンパイル / Compile LaTeX files
# Windowsの場合 / For Windows:
compile_simple.bat

# または手動で / Or manually:
pdflatex final_report.tex
pdflatex final_report.tex  # 2回実行（相互参照のため） / Run twice (for cross-references)
pdflatex poster.tex
pdflatex poster.tex
```

---

## 📊 評価指標 / Evaluation Metrics

1. **Feature Ranking Correlation**: Spearman相関係数（0-1、高いほど安定） / Spearman correlation coefficient (0-1, higher is more stable)
2. **SHAP Value Variance**: 分散（低いほど安定） / Variance (lower is more stable)
3. **Explanation Consistency**: Top-k特徴量の一貫性（%） / Top-k feature consistency (%)
4. **Faithfulness Metrics**: SHAP値と実際の特徴量重要度の相関 / Correlation between SHAP values and actual feature importance

---

## ⏱️ 実装時間の目安 / Estimated Implementation Time

- **データ準備**: 2-3時間 / Data preparation: 2-3 hours
- **モデル訓練**: 3-4時間 / Model training: 3-4 hours
- **SHAP実装**: 4-5時間 / SHAP implementation: 4-5 hours
- **安定性分析**: 5-6時間 / Stability analysis: 5-6 hours
- **可視化**: 3-4時間 / Visualization: 3-4 hours
- **コード整理**: 2-3時間 / Code organization: 2-3 hours
- **合計**: 約20-25時間 / Total: approximately 20-25 hours

---

## 📝 提出物 / Deliverables

1. **コード**: このフォルダ全体（GitHubにアップロード推奨） / Code: Entire folder (recommended to upload to GitHub)
2. **レポート**: PDF（10-15ページ） / Report: PDF (10-15 pages)
3. **ポスター**: PDF（1ページ） / Poster: PDF (1 page)
4. **プレゼンテーション**: 口頭試験用スライド / Presentation: Slides for oral examination

---

## 🔗 関連ファイル / Related Files

- **プロポーザル**: `../20_PROJECTS/interpretable-machine-learning-project-proposal.tex` / Proposal: `../20_PROJECTS/interpretable-machine-learning-project-proposal.tex`
- **試験対策**: `../20_PROJECTS/interpretable-machine-learning-exam-preparation.md` / Exam preparation: `../20_PROJECTS/interpretable-machine-learning-exam-preparation.md`
- **GitHubリポジトリ**: https://github.com/keisuke58/shap-stability-analysis / GitHub Repository: https://github.com/keisuke58/shap-stability-analysis

---

## 📚 主要な結果 / Key Results

このプロジェクトでは、以下の主要な結果を得ました：

This project obtained the following key results:

- **モデル比較**: XGBoost、Random Forest、Logistic RegressionのSHAP説明の安定性を比較 / **Model Comparison**: Compared stability of SHAP explanations for XGBoost, Random Forest, and Logistic Regression
- **サブサンプリング分析**: 異なるサンプルサイズ（50%, 75%, 100%）での安定性評価 / **Subsampling Analysis**: Stability evaluation with different sample sizes (50%, 75%, 100%)
- **安定性指標**: Feature Ranking Correlation、SHAP Value Variance、Explanation Consistencyを計算 / **Stability Metrics**: Calculated Feature Ranking Correlation, SHAP Value Variance, and Explanation Consistency

詳細は `final_report.pdf` と `poster.pdf` を参照してください。

For details, please refer to `final_report.pdf` and `poster.pdf`.

---

*最終更新 / Last updated: 2026-01-20*
