# Final Report and Poster

このディレクトリには、プロジェクトの最終レポートとポスターが含まれています。

## ファイル

- `final_report.tex`: 最終レポート（LaTeX形式）
- `poster.tex`: ポスター（LaTeX形式）
- `compile_documents.bat`: PDF生成用のバッチファイル（Windows）

## PDFの生成方法

### Windowsの場合

1. `compile_documents.bat` をダブルクリックして実行
2. または、コマンドプロンプトで以下を実行：
   ```bash
   pdflatex final_report.tex
   pdflatex final_report.tex
   pdflatex poster.tex
   pdflatex poster.tex
   ```

### Linux/Macの場合

```bash
pdflatex final_report.tex
pdflatex final_report.tex
pdflatex poster.tex
pdflatex poster.tex
```

## 必要なパッケージ

LaTeXコンパイルには以下のパッケージが必要です：
- `graphicx`: 図の挿入
- `booktabs`: 表の作成
- `amsmath`: 数式
- `xcolor`: 色の使用
- `geometry`: ページレイアウト
- `enumitem`: リストのカスタマイズ

## 結果ファイルの参照

レポートとポスターは以下の結果ファイルを参照しています：
- `results/figures/model_comparison.png`
- `results/figures/random_forest_shap_summary.png`
- `results/figures/xgboost_shap_summary.png`
- `results/tables/model_stability_comparison.csv`

これらのファイルが `results/` ディレクトリに存在することを確認してください。

## 注意事項

- ポスターはA0サイズ（landscape）で設計されています
- 図のパスが正しいことを確認してください
- コンパイルは2回実行することを推奨します（相互参照の解決のため）

## 内容

### 最終レポート (`final_report.tex`)

1. **Introduction**: 研究質問と動機
2. **Methodology**: データセット、モデル、評価指標
3. **Results**: 主要な結果と分析
4. **Discussion**: 結果の解釈と限界
5. **Conclusion**: 結論と今後の研究

### ポスター (`poster.tex`)

6つのセクションで構成：
1. **Introduction**: 研究質問と動機
2. **Key Results**: 主要な結果とメトリクス
3. **Methodology**: 実験設定
4. **Visualizations**: 主要な図
5. **Detailed Analysis**: 詳細な分析
6. **Conclusions & Recommendations**: 結論と推奨事項

## 現状の結果について

現在の結果は以下の通りです：
- モデル: 3種類（XGBoost, Random Forest, Logistic Regression）
- SHAPファイル: 15ファイル（各モデル5シード）
- 図: 13ファイル
- サブサンプリング結果: 未生成（今後の計算で追加可能）

レポートとポスターは現状の結果に基づいて作成されています。サブサンプリング結果が完成したら、必要に応じて更新できます。
