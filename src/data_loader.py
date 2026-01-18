"""
Data loading and preprocessing utilities
Student: Keisuke Nishioka (Matrikelnummer: 10081049)
"""

import pandas as pd
import numpy as np
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import warnings
warnings.filterwarnings('ignore')


def load_adult_income():
    """
    Load Adult Income dataset from UCI repository
    
    Returns:
        X: Features (DataFrame)
        y: Target (Series)
    """
    try:
        # Try to load from local file first
        df = pd.read_csv('data/raw/adult.csv')
    except FileNotFoundError:
        # Download from UCI
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data"
        columns = ['age', 'workclass', 'fnlwgt', 'education', 'education-num',
                  'marital-status', 'occupation', 'relationship', 'race', 'sex',
                  'capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'income']
        df = pd.read_csv(url, names=columns, na_values=' ?', skipinitialspace=True)
        df.to_csv('data/raw/adult.csv', index=False)
    
    # Preprocessing
    df = df.dropna()
    
    # Encode target
    le = LabelEncoder()
    df['income'] = le.fit_transform(df['income'])
    
    # Separate features and target
    X = df.drop('income', axis=1)
    y = df['income']
    
    # Encode categorical features
    X = pd.get_dummies(X, drop_first=True)
    
    return X, y


def load_boston_housing():
    """
    Load California Housing dataset (alternative to Boston Housing)
    
    Returns:
        X: Features (DataFrame)
        y: Target (Series)
    """
    data = fetch_california_housing()
    X = pd.DataFrame(data.data, columns=data.feature_names)
    y = pd.Series(data.target, name='target')
    return X, y


def load_wine_quality():
    """
    Load Wine Quality dataset from UCI repository
    
    Returns:
        X: Features (DataFrame)
        y: Target (Series)
    """
    try:
        df = pd.read_csv('data/raw/winequality-red.csv', sep=';')
    except FileNotFoundError:
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"
        df = pd.read_csv(url, sep=';')
        df.to_csv('data/raw/winequality-red.csv', index=False)
    
    X = df.drop('quality', axis=1)
    y = df['quality']
    
    # Convert to binary classification (quality >= 6)
    y = (y >= 6).astype(int)
    
    return X, y


def prepare_data(X, y, test_size=0.2, random_state=42):
    """
    Prepare data for training: split and scale
    
    Args:
        X: Features
        y: Target
        test_size: Test set size
        random_state: Random seed
    
    Returns:
        X_train, X_test, y_train, y_test, scaler
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y if y.dtype == 'int' else None
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = pd.DataFrame(
        scaler.fit_transform(X_train),
        columns=X_train.columns,
        index=X_train.index
    )
    X_test_scaled = pd.DataFrame(
        scaler.transform(X_test),
        columns=X_test.columns,
        index=X_test.index
    )
    
    return X_train_scaled, X_test_scaled, y_train, y_test, scaler


def subsample_data(X, y, rate=1.0, random_state=42):
    """
    Subsample data to specified rate
    
    Args:
        X: Features
        y: Target
        rate: Subsampling rate (0.0 to 1.0)
        random_state: Random seed
    
    Returns:
        X_subsampled, y_subsampled
    """
    if rate >= 1.0:
        return X, y
    
    n_samples = int(len(X) * rate)
    indices = np.random.RandomState(random_state).choice(
        len(X), size=n_samples, replace=False
    )
    
    return X.iloc[indices], y.iloc[indices]
