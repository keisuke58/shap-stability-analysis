# 実行手順と状況

## ✅ 実行状況

### 現在の状況
- **データ準備**: ✅ 完了
- **モデル訓練**: ✅ 完了（XGBoost 3モデル）
- **SHAP説明生成**: ⏳ 実行中（PermutationExplainer使用、時間がかかります）

---

## 🚀 実行方法

### 方法1: Quick Test（推奨・現在実行中）

```bash
cd C:\Users\nishi\Life\iML_Project_Stability_Analysis
python run_quick_test.py
```

**実行時間**: 約5-10分
- データ準備: 数秒
- モデル訓練: 約10-15秒
- SHAP説明生成: 約3-5分（PermutationExplainer）
- 安定性分析: 約1分

### 方法2: Jupyter Notebook（推奨）

各Notebookを順番に実行：

```bash
jupyter notebook notebooks/01_data_preprocessing.ipynb
# 実行後、次へ
jupyter notebook notebooks/02_model_training.ipynb
# ... 以下同様
```

### 方法3: フルパイプライン

```bash
python run_full_pipeline.py
```

**実行時間**: 約30-60分（CPU環境）

---

## ⚠️ 既知の問題と対処

### 問題1: XGBoostとSHAPの互換性

**症状**: TreeExplainerが直接使用できない
**現在の対処**: PermutationExplainerが自動的に使用される（遅いが動作する）

**改善案**:
1. SHAPを最新版にアップグレード（実施済み: v0.49.1）
2. XGBoostのバージョンを確認・調整
3. モデルの設定を変更

### 問題2: 実行時間が長い

**原因**: PermutationExplainerはTreeExplainerより遅い
**対処**: 
- テストサンプル数を減らす（`n_samples=30`など）
- CPU最適化設定を使用（`config_cpu.py`）

---

## 📊 実行結果の確認

実行が完了したら、以下を確認：

```bash
# SHAP値の確認
dir results\shap_values

# モデルの確認
dir results\models

# 結果の確認
dir results\tables
```

---

## 💡 次のステップ

1. **Quick Testの完了を待つ**
   - 現在実行中（約3-5分）

2. **結果の確認**
   - SHAP値が正しく生成されているか確認

3. **フル実装の実行**
   - Quick Testが成功したら、フル実装を実行
   - または、Notebookを順番に実行

---

## 🔧 トラブルシューティング

### エラー: ModuleNotFoundError
```bash
pip install -r requirements.txt
```

### エラー: SHAPの計算が遅い
- 正常です。PermutationExplainerは時間がかかります
- 完了まで待つか、サンプル数を減らしてください

### エラー: メモリ不足
- テストサンプル数を減らす（`n_samples`を減らす）
- データセットのサイズを減らす

---

*実行は継続中です。完了までお待ちください。*
