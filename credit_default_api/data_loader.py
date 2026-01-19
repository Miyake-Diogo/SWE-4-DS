"""
Data loader for UCI Credit Card Default Dataset
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from typing import Tuple


def load_credit_default_data() -> Tuple[pd.DataFrame, pd.Series]:
    """
    Load the UCI Credit Card Default dataset.
    
    Returns:
        Tuple of (features DataFrame, target Series)
    """
    try:
        from ucimlrepo import fetch_ucirepo
        
        # Fetch dataset from UCI ML Repository
        # ID 350: Default of Credit Card Clients Dataset
        credit_default = fetch_ucirepo(id=350)
        
        X = credit_default.data.features
        y = credit_default.data.targets
        
        # Convert to pandas if needed
        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame(X)
        if not isinstance(y, pd.Series):
            y = pd.Series(y.values.ravel())
            
    except Exception as e:
        print(f"Error fetching from UCI: {e}")
        print("Generating synthetic data for demonstration...")
        X, y = generate_synthetic_data()
    
    return X, y


def generate_synthetic_data(n_samples: int = 5000) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Generate synthetic credit default data for demonstration.
    
    Args:
        n_samples: Number of samples to generate
        
    Returns:
        Tuple of (features DataFrame, target Series)
    """
    np.random.seed(42)
    
    # Generate synthetic features
    data = {
        'LIMIT_BAL': np.random.randint(10000, 500000, n_samples),
        'SEX': np.random.randint(1, 3, n_samples),
        'EDUCATION': np.random.randint(1, 5, n_samples),
        'MARRIAGE': np.random.randint(1, 4, n_samples),
        'AGE': np.random.randint(21, 75, n_samples),
        'PAY_0': np.random.randint(-2, 9, n_samples),
        'PAY_2': np.random.randint(-2, 9, n_samples),
        'PAY_3': np.random.randint(-2, 9, n_samples),
        'PAY_4': np.random.randint(-2, 9, n_samples),
        'PAY_5': np.random.randint(-2, 9, n_samples),
        'PAY_6': np.random.randint(-2, 9, n_samples),
        'BILL_AMT1': np.random.randint(0, 100000, n_samples),
        'BILL_AMT2': np.random.randint(0, 100000, n_samples),
        'BILL_AMT3': np.random.randint(0, 100000, n_samples),
        'BILL_AMT4': np.random.randint(0, 100000, n_samples),
        'BILL_AMT5': np.random.randint(0, 100000, n_samples),
        'BILL_AMT6': np.random.randint(0, 100000, n_samples),
        'PAY_AMT1': np.random.randint(0, 50000, n_samples),
        'PAY_AMT2': np.random.randint(0, 50000, n_samples),
        'PAY_AMT3': np.random.randint(0, 50000, n_samples),
        'PAY_AMT4': np.random.randint(0, 50000, n_samples),
        'PAY_AMT5': np.random.randint(0, 50000, n_samples),
        'PAY_AMT6': np.random.randint(0, 50000, n_samples),
    }
    
    X = pd.DataFrame(data)
    
    # Generate target with some logic
    default_prob = (
        (X['PAY_0'] > 2).astype(int) * 0.3 +
        (X['PAY_2'] > 2).astype(int) * 0.2 +
        (X['AGE'] < 30).astype(int) * 0.1 +
        np.random.random(n_samples) * 0.4
    )
    y = (default_prob > 0.5).astype(int)
    y = pd.Series(y, name='default')
    
    return X, y


def preprocess_data(
    X: pd.DataFrame,
    y: pd.Series,
    test_size: float = 0.2,
    random_state: int = 42
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, StandardScaler]:
    """
    Preprocess the data: split and scale.
    
    Args:
        X: Feature DataFrame
        y: Target Series
        test_size: Proportion of test set
        random_state: Random seed
        
    Returns:
        Tuple of (X_train, X_test, y_train, y_test, scaler)
    """
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    return X_train_scaled, X_test_scaled, y_train.values, y_test.values, scaler


if __name__ == "__main__":
    # Test data loading
    print("Loading credit default data...")
    X, y = load_credit_default_data()
    print(f"Data shape: {X.shape}")
    print(f"Features: {X.columns.tolist()}")
    print(f"Target distribution:\n{y.value_counts()}")
    
    print("\nPreprocessing data...")
    X_train, X_test, y_train, y_test, scaler = preprocess_data(X, y)
    print(f"Train set: {X_train.shape}, Test set: {X_test.shape}")
