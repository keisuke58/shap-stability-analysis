# CPU環境での実行ガイド

## ✅ CPU環境で動作します

実装したコードは**CPU環境で完全に動作します**。GPUは不要です。

---

## ⚙️ CPU環境での最適化設定

### 1. 設定ファイルの調整

`config.py` を編集して、CPU環境に最適化：

```python
# CPU環境用の設定（config.pyに追加または変更）

# ランダムシード数（CPU環境では少なめに）
RANDOM_SEEDS = [42, 123, 456, 789, 1011]  # 10個 → 5個に削減

# SHAP設定（CPU環境用）
SHAP_CONFIG = {
    'tree_explainer': {
        'check_additivity': False
    },
    'kernel_explainer': {
        'nsamples': 50,  # 100 → 50に削減（KernelSHAPは時間がかかる）
        'l1_reg': 'auto'
    }
}

# 安定性分析設定
STABILITY_CONFIG = {
    'top_k_features': [3, 5, 10],
    'n_test_samples': 50,  # 100 → 50に削減（計算時間短縮）
    'correlation_method': 'spearman'
}
```

### 2. モデル訓練の最適化

CPU環境では、モデルのパラメータを調整：

```python
# XGBoost（CPU環境用）
MODELS = {
    'xgboost': {
        'n_estimators': 50,  # 100 → 50に削減
        'max_depth': 5,      # 6 → 5に削減
        'n_jobs': -1         # 全CPUコアを使用
    },
    'random_forest': {
        'n_estimators': 50,  # 100 → 50に削減
        'max_depth': 8,      # 10 → 8に削減
        'n_jobs': -1         # 全CPUコアを使用
    }
}
```

---

## ⏱️ CPU環境での実行時間見積もり

### 最小実装（合格レベル）

| ステップ | 時間（CPU環境） | 最適化後 |
|---------|----------------|---------|
| データ準備 | 2-3分 | 2-3分 |
| モデル訓練（3モデル×5シード） | 10-15分 | 5-8分 |
| TreeSHAP（XGBoost, RF） | 5-10分 | 3-5分 |
| KernelSHAP（Logistic Regression×5シード） | 30-60分 | 15-30分 |
| 安定性分析 | 2-3分 | 2-3分 |
| 可視化 | 2-3分 | 2-3分 |
| **合計** | **約50-90分** | **約30-55分** |

### 推奨実装（良い成績）

- 上記 + 全モデル分析 + サブサンプリング分析
- **合計: 約2-3時間**（最適化後）

---

## 🚀 CPU環境での実行方法

### 方法1: 最適化設定で実行

1. **設定ファイルを編集**
   ```python
   # config.py を編集
   RANDOM_SEEDS = [42, 123, 456, 789, 1011]  # 5個に削減
   STABILITY_CONFIG['n_test_samples'] = 50   # 50に削減
   SHAP_CONFIG['kernel_explainer']['nsamples'] = 50  # 50に削減
   ```

2. **Notebookを実行**
   - 各Notebookを順番に実行
   - KernelSHAPは時間がかかるので、最初は3シード程度でテスト

### 方法2: 段階的に実行（推奨）

1. **まずXGBoostのみでテスト**
   ```python
   # 02_model_training.ipynb で
   # XGBoostのみ訓練（5シード）
   # Random ForestとLogistic Regressionは後で
   ```

2. **TreeSHAPのみでテスト**
   ```python
   # 03_shap_explanations.ipynb で
   # XGBoostとRandom Forestのみ（TreeSHAPは高速）
   # KernelSHAPは後で
   ```

3. **KernelSHAPは最後に**
   ```python
   # KernelSHAPは時間がかかるので、最後に実行
   # 最初は3シード程度でテスト
   ```

---

## 💡 CPU環境での最適化のコツ

### 1. 並列処理を活用

- `n_jobs=-1` を設定して全CPUコアを使用
- XGBoost, Random Forestは自動的に並列処理

### 2. データサイズを調整

- 最初は小さなデータセットでテスト
- 動作確認後、フルデータセットで実行

### 3. KernelSHAPの最適化

- `nsamples` を減らす（50-100程度）
- 背景サンプル数を減らす（50-100程度）
- 最初は少ないシードで実行

### 4. メモリ管理

- 大きなデータセットは分割して処理
- 中間結果を保存して再利用

---

## ⚠️ CPU環境での注意事項

### 1. KernelSHAPは時間がかかる

- **TreeSHAP**: 高速（数秒〜数分）
- **KernelSHAP**: 遅い（数十分〜数時間）

**対策**:
- 最初は少ないシードで実行（3-5個）
- `nsamples` を減らす（50程度）
- テストサンプル数を減らす（50程度）

### 2. メモリ使用量

- 大きなデータセットではメモリ不足の可能性
- データを分割して処理

### 3. 計算時間

- フル実装は数時間かかる可能性
- 段階的に実行して進捗を確認

---

## 📊 推奨実行順序（CPU環境）

### Phase 1: 基本実装（約1時間）

1. **データ準備** (5分)
   - `01_data_preprocessing.ipynb`

2. **モデル訓練（XGBoostのみ）** (10分)
   - `02_model_training.ipynb` - XGBoostのみ実行

3. **TreeSHAP（XGBoost）** (5分)
   - `03_shap_explanations.ipynb` - XGBoostのみ実行

4. **安定性分析（XGBoost）** (5分)
   - `04_stability_analysis.ipynb` - XGBoostのみ実行

5. **可視化** (5分)
   - `05_visualization.ipynb`

### Phase 2: 拡張（時間があれば）

6. **Random Forest追加** (+20分)
7. **Logistic Regression追加** (+30-60分)

---

## ✅ CPU環境での動作確認

以下のコマンドで動作確認：

```bash
# 環境セットアップ
pip install -r requirements.txt

# 簡単なテスト
python -c "from src.data_loader import load_adult_income; X, y = load_adult_income(); print(f'Data loaded: {X.shape}')"

# モデル訓練テスト（小規模）
python -c "from src.models import train_xgboost; from src.data_loader import load_adult_income, prepare_data; X, y = load_adult_income(); X_train, X_test, y_train, y_test, _ = prepare_data(X, y); model = train_xgboost(X_train, y_train, random_state=42); print('Model trained successfully!')"
```

---

## 🎯 結論

**CPU環境で完全に動作します！**

- ✅ GPU不要
- ✅ すべてのライブラリがCPU対応
- ⚠️ KernelSHAPは時間がかかる（CPUでも動作）
- 💡 設定を最適化すれば、約1-2時間で基本実装完了

**推奨**: 最初は最適化設定で実行し、動作確認後にフル実装を実行してください。
