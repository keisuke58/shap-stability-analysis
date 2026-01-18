# CPU環境での実行ガイド

## ✅ CPU環境で完全に動作します

実装したコードは**GPU不要で、CPU環境で完全に動作します**。

使用しているライブラリはすべてCPU対応：
- ✅ **XGBoost**: CPUで動作（デフォルト）
- ✅ **scikit-learn**: CPUのみ（Random Forest, Logistic Regression）
- ✅ **SHAP**: CPUで動作（TreeSHAPは高速、KernelSHAPは遅いがCPUで動作）
- ✅ **その他**: pandas, numpy, matplotlib等、すべてCPU対応

---

## ⚙️ CPU環境での最適化

### 方法1: CPU最適化設定ファイルを使用（推奨）

```python
# Notebookやスクリプトで、configの代わりにconfig_cpuを使用
import config_cpu as config
```

`config_cpu.py` の主な最適化：
- ランダムシード数: 10個 → 5個
- テストサンプル数: 100 → 50
- KernelSHAPサンプル数: 100 → 50
- モデルパラメータ: 削減（n_estimators: 100 → 50）

### 方法2: 手動で設定を調整

`config.py` を編集：
```python
# ランダムシード数を減らす
RANDOM_SEEDS = [42, 123, 456, 789, 1011]  # 5個

# テストサンプル数を減らす
STABILITY_CONFIG['n_test_samples'] = 50  # 50に削減

# KernelSHAPのサンプル数を減らす
SHAP_CONFIG['kernel_explainer']['nsamples'] = 50  # 50に削減
```

---

## ⏱️ CPU環境での実行時間見積もり

### 最小実装（合格レベル・最適化後）

| ステップ | 時間 |
|---------|------|
| データ準備 | 2-3分 |
| モデル訓練（3モデル×5シード） | 5-8分 |
| TreeSHAP（XGBoost, RF） | 3-5分 |
| KernelSHAP（Logistic Regression×5シード） | 15-30分 |
| 安定性分析 | 2-3分 |
| 可視化 | 2-3分 |
| **合計** | **約30-55分** |

### 推奨実装（良い成績）

- 上記 + 全モデル分析 + サブサンプリング分析
- **合計: 約1.5-2.5時間**

---

## 🚀 CPU環境での実行方法

### 推奨：段階的に実行

#### Step 1: まずXGBoostのみでテスト（約15分）

1. **データ準備** (3分)
   ```bash
   jupyter notebook notebooks/01_data_preprocessing.ipynb
   ```

2. **XGBoost訓練** (5分)
   ```bash
   jupyter notebook notebooks/02_model_training.ipynb
   # XGBoostのみ実行（Random ForestとLogistic Regressionは後で）
   ```

3. **TreeSHAP（XGBoost）** (3分)
   ```bash
   jupyter notebook notebooks/03_shap_explanations.ipynb
   # XGBoostのみ実行
   ```

4. **安定性分析（XGBoost）** (2分)
   ```bash
   jupyter notebook notebooks/04_stability_analysis.ipynb
   ```

5. **可視化** (2分)
   ```bash
   jupyter notebook notebooks/05_visualization.ipynb
   ```

#### Step 2: 他のモデルを追加（時間があれば）

- Random Forest追加: +10-15分
- Logistic Regression追加: +20-40分（KernelSHAPは時間がかかる）

---

## 💡 CPU環境での最適化のコツ

### 1. 並列処理を活用

- `n_jobs=-1` で全CPUコアを使用（既に設定済み）
- XGBoost, Random Forestは自動的に並列処理

### 2. KernelSHAPの最適化

- **最初は少ないシードで実行**（3-5個）
- **`nsamples` を減らす**（50程度）
- **テストサンプル数を減らす**（50程度）

### 3. 段階的に実行

- まずXGBoostのみで動作確認
- 動作確認後、他のモデルを追加

---

## ⚠️ 注意事項

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

---

## 📊 推奨実行順序（CPU環境）

### Phase 1: 基本実装（約30-55分）

1. ✅ データ準備
2. ✅ XGBoost訓練（5シード）
3. ✅ TreeSHAP（XGBoost）
4. ✅ 安定性分析（XGBoost）
5. ✅ 可視化

**これで最低限の実装は完了！**

### Phase 2: 拡張（時間があれば）

6. Random Forest追加
7. Logistic Regression追加（KernelSHAP）

---

## ✅ 動作確認

```bash
# 環境セットアップ
pip install -r requirements.txt

# 簡単なテスト
python -c "from src.data_loader import load_adult_income; X, y = load_adult_income(); print(f'Data loaded: {X.shape}')"
```

---

## 🎯 結論

**CPU環境で完全に動作します！**

- ✅ GPU不要
- ✅ すべてのライブラリがCPU対応
- ⚠️ KernelSHAPは時間がかかる（CPUでも動作）
- 💡 最適化設定を使用すれば、約30-55分で基本実装完了

**推奨**: 
1. まず `config_cpu.py` を使用して最適化設定で実行
2. 動作確認後、必要に応じてフル実装を実行

詳細は `CPU_OPTIMIZATION.md` を参照してください。
