# SHAP Stability Analysis Project

**Project Title**: Stability and Faithfulness Analysis of SHAP Explanations for Tabular Models  
**Course**: Interpretierbares Maschinelles Lernen (Interpretable Machine Learning)  
**Student**: Keisuke Nishioka (Matrikelnummer: 10081049)  
**Instructor**: Prof. Dr. rer. nat. Marius Lindauer

---

## 📋 プロジェクト概要

このプロジェクトでは、SHAP説明の安定性と信頼性を分析します。異なるランダムシード、データサブサンプリング、モデルクラスにおけるSHAP説明の一貫性を評価します。

---

## 🎯 実装範囲（どこまでやるか）

### ✅ 実装すべき内容

#### Phase 1: データ準備とモデル訓練
- [x] データセットの選択と読み込み
- [x] データ前処理（欠損値処理、エンコーディング）
- [x] 3つのモデルの実装と訓練
  - XGBoost (TreeSHAP)
  - Random Forest (TreeSHAP)
  - Logistic Regression (KernelSHAP)

#### Phase 2: SHAP説明の生成
- [x] TreeSHAPの実装（XGBoost, Random Forest用）
- [x] KernelSHAPの実装（Logistic Regression用）
- [x] 複数のランダムシードでの説明生成
- [x] 異なるデータサブサンプリング率での説明生成

#### Phase 3: 安定性分析
- [x] Feature Ranking Correlation（Spearman相関）の計算
- [x] SHAP Value Varianceの計算
- [x] Explanation Consistency（top-k特徴量の一貫性）の計算
- [x] モデル間比較
- [x] サンプルサイズ効果の分析

#### Phase 4: 可視化
- [x] SHAP summary plots
- [x] Feature ranking correlation heatmaps
- [x] SHAP value variance box plots
- [x] Stability comparison across models
- [x] Sample size effect visualizations

#### Phase 5: 結果のまとめ
- [x] 安定性条件の特定
- [x] 実用的な推奨事項の整理
- [x] 結果の解釈と考察

### ❌ 実装しない内容（スコープ外）

- 新規アルゴリズムの開発
- LIMEや他の手法との比較
- 画像・テキストデータの処理
- 高計算コストモデル（Deep Learning等）

---

## 📁 プロジェクト構造

```
iML_Project_Stability_Analysis/
├── README.md                          # このファイル
├── requirements.txt                   # Python依存パッケージ
├── config.py                          # 設定ファイル（random seeds, データセット等）
│
├── data/                              # データセット
│   ├── raw/                           # 生データ
│   └── processed/                      # 前処理済みデータ
│
├── notebooks/                         # Jupyter Notebooks
│   ├── 01_data_preprocessing.ipynb    # データ前処理
│   ├── 02_model_training.ipynb       # モデル訓練
│   ├── 03_shap_explanations.ipynb    # SHAP説明生成
│   ├── 04_stability_analysis.ipynb   # 安定性分析
│   └── 05_visualization.ipynb        # 可視化
│
├── src/                               # Pythonモジュール
│   ├── __init__.py
│   ├── data_loader.py                 # データ読み込み
│   ├── models.py                      # モデル定義と訓練
│   ├── shap_analysis.py              # SHAP説明生成
│   ├── stability_metrics.py           # 安定性指標の計算
│   └── visualization.py              # 可視化関数
│
├── results/                           # 結果ファイル
│   ├── figures/                       # 図表（PNG/PDF）
│   ├── tables/                        # 表（CSV）
│   └── shap_values/                  # 保存されたSHAP値（NPZ）
│
├── reports/                           # レポート関連
│   └── (最終レポートは別途作成)
│
└── .gitignore                         # Git除外ファイル
```

---

## 🚀 実装の進め方

### Step 1: 環境セットアップ
```bash
# 仮想環境作成（推奨）
python -m venv venv
venv\Scripts\activate  # Windows

# 依存パッケージインストール
pip install -r requirements.txt
```

### Step 2: データ準備
- `notebooks/01_data_preprocessing.ipynb` を実行
- データセットを `data/raw/` に配置

### Step 3: モデル訓練
- `notebooks/02_model_training.ipynb` を実行
- 複数のランダムシードで訓練

### Step 4: SHAP説明生成
- `notebooks/03_shap_explanations.ipynb` を実行
- TreeSHAPとKernelSHAPの両方を実装

### Step 5: 安定性分析
- `notebooks/04_stability_analysis.ipynb` を実行
- 評価指標を計算

### Step 6: 可視化
- `notebooks/05_visualization.ipynb` を実行
- 結果を `results/figures/` に保存

---

## 📊 評価指標

1. **Feature Ranking Correlation**: Spearman相関係数（0-1、高いほど安定）
2. **SHAP Value Variance**: 分散（低いほど安定）
3. **Explanation Consistency**: Top-k特徴量の一貫性（%）
4. **Faithfulness Metrics**: SHAP値と実際の特徴量重要度の相関

---

## ⏱️ 実装時間の目安

- **データ準備**: 2-3時間
- **モデル訓練**: 3-4時間
- **SHAP実装**: 4-5時間
- **安定性分析**: 5-6時間
- **可視化**: 3-4時間
- **コード整理**: 2-3時間
- **合計**: 約20-25時間

---

## 📝 提出物

1. **コード**: このフォルダ全体（GitHubにアップロード推奨）
2. **レポート**: PDF（10-15ページ）
3. **プレゼンテーション**: 口頭試験用スライド

---

## 🔗 関連ファイル

- **プロポーザル**: `../20_PROJECTS/interpretable-machine-learning-project-proposal.md`
- **試験対策**: `../20_PROJECTS/interpretable-machine-learning-exam-preparation.md`

---

*最終更新: 2026-01-20*
