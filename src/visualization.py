"""
Visualization utilities for SHAP stability analysis
Student: Keisuke Nishioka (Matrikelnummer: 10081049)
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import shap
import os


def setup_plot_style():
    """Setup matplotlib style"""
    plt.style.use('seaborn-v0_8')
    sns.set_palette("husl")
    plt.rcParams['figure.figsize'] = (10, 6)
    plt.rcParams['font.size'] = 12
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10


def plot_shap_summary(shap_values, X_sample, feature_names=None, save_path=None):
    """
    Plot SHAP summary plot
    
    Args:
        shap_values: SHAP values array
        X_sample: Sample features
        feature_names: Feature names (optional)
        save_path: Path to save figure (optional)
    """
    setup_plot_style()
    
    # Create SHAP Explanation object
    if feature_names is None and hasattr(X_sample, 'columns'):
        feature_names = X_sample.columns.tolist()
    
    shap_explanation = shap.Explanation(
        values=shap_values,
        base_values=np.zeros(len(shap_values)),
        data=X_sample.values if hasattr(X_sample, 'values') else X_sample,
        feature_names=feature_names
    )
    
    plt.figure(figsize=(10, 8))
    shap.plots.beeswarm(shap_explanation, show=False)
    plt.tight_layout()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return plt.gcf()


def plot_ranking_correlation(stability_metrics, save_path=None):
    """
    Plot feature ranking correlation distribution
    
    Args:
        stability_metrics: Stability metrics dictionary
        save_path: Path to save figure (optional)
    """
    setup_plot_style()
    
    correlations = stability_metrics['ranking_correlation']['per_sample']
    
    plt.figure(figsize=(8, 6))
    plt.hist(correlations, bins=20, edgecolor='black', alpha=0.7)
    plt.axvline(np.mean(correlations), color='red', linestyle='--', 
                label=f'Mean: {np.mean(correlations):.3f}')
    plt.xlabel('Spearman Correlation Coefficient')
    plt.ylabel('Frequency')
    plt.title('Distribution of Feature Ranking Correlations')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return plt.gcf()


def plot_shap_variance(stability_metrics, feature_names=None, top_n=10, save_path=None):
    """
    Plot SHAP value variance by feature
    
    Args:
        stability_metrics: Stability metrics dictionary
        feature_names: Feature names (optional)
        top_n: Number of top features to show
        save_path: Path to save figure (optional)
    """
    setup_plot_style()
    
    variance_per_feature = stability_metrics['variance']['per_feature']
    
    # Get top-n features with highest variance
    top_indices = np.argsort(variance_per_feature)[-top_n:][::-1]
    top_variance = variance_per_feature[top_indices]
    
    if feature_names is None:
        feature_names = [f'Feature {i}' for i in range(len(variance_per_feature))]
    
    top_feature_names = [feature_names[int(i)] for i in top_indices]
    
    plt.figure(figsize=(10, 6))
    plt.barh(range(len(top_variance)), top_variance)
    plt.yticks(range(len(top_variance)), top_feature_names)
    plt.xlabel('SHAP Value Variance')
    plt.title(f'Top {top_n} Features by SHAP Value Variance')
    plt.gca().invert_yaxis()
    plt.grid(True, alpha=0.3, axis='x')
    plt.tight_layout()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return plt.gcf()


def plot_consistency_comparison(stability_metrics, top_k_list=[3, 5, 10], save_path=None):
    """
    Plot consistency comparison for different top-k values
    
    Args:
        stability_metrics: Stability metrics dictionary
        top_k_list: List of top-k values
        save_path: Path to save figure (optional)
    """
    setup_plot_style()
    
    consistency_values = [
        stability_metrics['consistency'][f'top_{k}']['overall'] 
        for k in top_k_list
    ]
    
    plt.figure(figsize=(8, 6))
    plt.bar(range(len(top_k_list)), consistency_values, alpha=0.7, edgecolor='black')
    plt.xticks(range(len(top_k_list)), [f'Top-{k}' for k in top_k_list])
    plt.ylabel('Consistency (%)')
    plt.xlabel('Top-k Features')
    plt.title('Explanation Consistency Across Different Top-k Values')
    plt.ylim([0, 1])
    plt.grid(True, alpha=0.3, axis='y')
    
    # Add value labels
    for i, v in enumerate(consistency_values):
        plt.text(i, v + 0.02, f'{v:.3f}', ha='center', va='bottom')
    
    plt.tight_layout()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return plt.gcf()


def plot_model_comparison(comparison_df, save_path=None):
    """
    Plot comparison of stability metrics across models
    
    Args:
        comparison_df: DataFrame with model comparison
        save_path: Path to save figure (optional)
    """
    setup_plot_style()
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Ranking Correlation
    axes[0, 0].bar(comparison_df['Model'], comparison_df['Ranking Correlation'], alpha=0.7)
    axes[0, 0].set_ylabel('Ranking Correlation')
    axes[0, 0].set_title('Feature Ranking Correlation')
    axes[0, 0].tick_params(axis='x', rotation=45)
    axes[0, 0].grid(True, alpha=0.3, axis='y')
    
    # SHAP Variance
    axes[0, 1].bar(comparison_df['Model'], comparison_df['SHAP Variance'], alpha=0.7, color='orange')
    axes[0, 1].set_ylabel('SHAP Variance')
    axes[0, 1].set_title('SHAP Value Variance')
    axes[0, 1].tick_params(axis='x', rotation=45)
    axes[0, 1].grid(True, alpha=0.3, axis='y')
    
    # Top-5 Consistency
    axes[1, 0].bar(comparison_df['Model'], comparison_df['Top-5 Consistency'], alpha=0.7, color='green')
    axes[1, 0].set_ylabel('Consistency')
    axes[1, 0].set_title('Top-5 Feature Consistency')
    axes[1, 0].tick_params(axis='x', rotation=45)
    axes[1, 0].grid(True, alpha=0.3, axis='y')
    
    # Combined metrics (normalized)
    metrics_norm = comparison_df[['Ranking Correlation', 'Top-5 Consistency']].copy()
    metrics_norm['SHAP Variance (inverted)'] = 1 / (1 + comparison_df['SHAP Variance'])
    metrics_norm.plot(kind='bar', ax=axes[1, 1], width=0.8)
    axes[1, 1].set_ylabel('Normalized Score')
    axes[1, 1].set_title('Combined Stability Metrics (Normalized)')
    axes[1, 1].set_xticklabels(comparison_df['Model'], rotation=45)
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig
