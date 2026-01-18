"""
Stability metrics computation utilities
Student: Keisuke Nishioka (Matrikelnummer: 10081049)
"""

import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from scipy.spatial.distance import pdist, squareform
from tqdm import tqdm


def compute_feature_ranking(shap_values):
    """
    Compute feature ranking from SHAP values
    
    Args:
        shap_values: SHAP values array (n_samples, n_features)
    
    Returns:
        Feature rankings (n_samples, n_features) - lower rank = more important
    """
    # Compute absolute SHAP values
    abs_shap = np.abs(shap_values)
    
    # Rank features (1 = most important)
    rankings = np.argsort(np.argsort(-abs_shap, axis=1), axis=1) + 1
    
    return rankings


def compute_ranking_correlation(rankings_list):
    """
    Compute Spearman correlation of feature rankings across different runs
    
    Args:
        rankings_list: List of ranking arrays from different runs
    
    Returns:
        Mean correlation coefficient and correlation matrix
    """
    n_runs = len(rankings_list)
    n_samples = rankings_list[0].shape[0]
    
    correlations = []
    
    for sample_idx in range(n_samples):
        sample_rankings = [rankings[sample_idx, :] for rankings in rankings_list]
        
        # Compute pairwise correlations
        sample_corrs = []
        for i in range(n_runs):
            for j in range(i + 1, n_runs):
                corr, _ = spearmanr(sample_rankings[i], sample_rankings[j])
                sample_corrs.append(corr)
        
        correlations.append(np.mean(sample_corrs))
    
    return np.mean(correlations), correlations


def compute_shap_variance(shap_values_list):
    """
    Compute variance of SHAP values across different runs
    
    Args:
        shap_values_list: List of SHAP value arrays from different runs
    
    Returns:
        Mean variance per feature and per sample
    """
    # Stack all SHAP values
    shap_stack = np.stack(shap_values_list, axis=0)  # (n_runs, n_samples, n_features)
    
    # Compute variance across runs
    variance = np.var(shap_stack, axis=0)  # (n_samples, n_features)
    
    # Mean variance per feature
    mean_variance_per_feature = np.mean(variance, axis=0)
    
    # Mean variance per sample
    mean_variance_per_sample = np.mean(variance, axis=1)
    
    # Overall mean variance
    overall_mean_variance = np.mean(variance)
    
    return {
        'per_feature': mean_variance_per_feature,
        'per_sample': mean_variance_per_sample,
        'overall': overall_mean_variance,
        'full_variance': variance
    }


def compute_explanation_consistency(rankings_list, top_k=5):
    """
    Compute consistency of top-k features across different runs
    
    Args:
        rankings_list: List of ranking arrays from different runs
        top_k: Number of top features to consider
    
    Returns:
        Consistency percentage per sample and overall
    """
    n_runs = len(rankings_list)
    n_samples = rankings_list[0].shape[0]
    n_features = rankings_list[0].shape[1]
    
    consistencies = []
    
    for sample_idx in range(n_samples):
        # Get top-k features for each run
        top_k_features = []
        for rankings in rankings_list:
            top_k_indices = np.argsort(rankings[sample_idx, :])[:top_k]
            top_k_features.append(set(top_k_indices.flatten().tolist()))  # Flatten and convert to list
        
        # Compute intersection of top-k features across all runs
        intersection = set.intersection(*top_k_features)
        
        # Consistency = size of intersection / top_k
        consistency = len(intersection) / top_k
        consistencies.append(consistency)
    
    return {
        'per_sample': np.array(consistencies),
        'overall': np.mean(consistencies)
    }


def compute_stability_metrics(shap_values_dict, top_k_list=[3, 5, 10]):
    """
    Compute all stability metrics for SHAP values from multiple runs
    
    Args:
        shap_values_dict: Dictionary {seed: shap_values}
        top_k_list: List of top-k values for consistency analysis
    
    Returns:
        Dictionary of all stability metrics
    """
    # Extract SHAP values and seeds
    seeds = sorted(shap_values_dict.keys())
    shap_values_list = []
    for seed in seeds:
        shap_vals = shap_values_dict[seed]
        # Handle 3D SHAP values (n_samples, n_features, n_classes)
        if len(shap_vals.shape) == 3:
            shap_vals = shap_vals[:, :, 1] if shap_vals.shape[2] > 1 else shap_vals[:, :, 0]
        shap_values_list.append(shap_vals)
    
    # Compute rankings
    rankings_list = [compute_feature_ranking(shap_vals) for shap_vals in shap_values_list]
    
    # Compute metrics
    ranking_corr_mean, ranking_corrs = compute_ranking_correlation(rankings_list)
    variance_metrics = compute_shap_variance(shap_values_list)
    
    consistency_metrics = {}
    for top_k in top_k_list:
        consistency_metrics[f'top_{top_k}'] = compute_explanation_consistency(rankings_list, top_k=top_k)
    
    return {
        'ranking_correlation': {
            'mean': ranking_corr_mean,
            'per_sample': ranking_corrs
        },
        'variance': variance_metrics,
        'consistency': consistency_metrics,
        'n_runs': len(seeds),
        'n_samples': shap_values_list[0].shape[0],
        'n_features': shap_values_list[0].shape[1]
    }


def compare_models_stability(stability_results_dict):
    """
    Compare stability metrics across different models
    
    Args:
        stability_results_dict: Dictionary {model_name: stability_metrics}
    
    Returns:
        Comparison DataFrame
    """
    comparison_data = []
    
    for model_name, metrics in stability_results_dict.items():
        comparison_data.append({
            'Model': model_name,
            'Ranking Correlation': metrics['ranking_correlation']['mean'],
            'SHAP Variance': metrics['variance']['overall'],
            'Top-3 Consistency': metrics['consistency']['top_3']['overall'],
            'Top-5 Consistency': metrics['consistency']['top_5']['overall'],
            'Top-10 Consistency': metrics['consistency']['top_10']['overall']
        })
    
    return pd.DataFrame(comparison_data)
