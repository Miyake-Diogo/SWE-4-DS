"""
Training pipeline with MLflow tracking for Credit Card Default prediction
"""
import mlflow
import mlflow.sklearn
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
    confusion_matrix
)
import pandas as pd
import numpy as np
import joblib
import os
from data_loader import load_credit_default_data, preprocess_data


def train_decision_tree(
    max_depth: int = 10,
    min_samples_split: int = 20,
    min_samples_leaf: int = 10,
    criterion: str = 'gini',
    random_state: int = 42
):
    """
    Train Decision Tree classifier with MLflow tracking.
    
    Args:
        max_depth: Maximum depth of the tree
        min_samples_split: Minimum samples required to split
        min_samples_leaf: Minimum samples required at leaf node
        criterion: Split quality measure ('gini' or 'entropy')
        random_state: Random seed
    """
    
    # Set MLflow tracking URI (will use local mlruns folder)
    mlflow.set_tracking_uri("file:./mlruns")
    mlflow.set_experiment("credit_default_prediction")
    
    print("=" * 80)
    print("CREDIT CARD DEFAULT PREDICTION - DECISION TREE MODEL")
    print("=" * 80)
    
    # Start MLflow run
    with mlflow.start_run(run_name="decision_tree_baseline"):
        
        # Load and preprocess data
        print("\n1. Loading dataset...")
        X, y = load_credit_default_data()
        print(f"   Dataset shape: {X.shape}")
        print(f"   Default rate: {y.mean():.2%}")
        
        print("\n2. Preprocessing data...")
        X_train, X_test, y_train, y_test, scaler = preprocess_data(X, y)
        print(f"   Train samples: {len(X_train)}")
        print(f"   Test samples: {len(X_test)}")
        
        # Log parameters
        params = {
            "model_type": "DecisionTreeClassifier",
            "max_depth": max_depth,
            "min_samples_split": min_samples_split,
            "min_samples_leaf": min_samples_leaf,
            "criterion": criterion,
            "random_state": random_state,
            "n_features": X.shape[1],
            "n_samples_train": len(X_train),
            "n_samples_test": len(X_test)
        }
        mlflow.log_params(params)
        
        # Train model
        print("\n3. Training Decision Tree model...")
        model = DecisionTreeClassifier(
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            min_samples_leaf=min_samples_leaf,
            criterion=criterion,
            random_state=random_state
        )
        model.fit(X_train, y_train)
        print("   Training complete!")
        
        # Make predictions
        print("\n4. Evaluating model...")
        y_train_pred = model.predict(X_train)
        y_test_pred = model.predict(X_test)
        y_test_proba = model.predict_proba(X_test)[:, 1]
        
        # Calculate metrics
        metrics = {
            "train_accuracy": accuracy_score(y_train, y_train_pred),
            "test_accuracy": accuracy_score(y_test, y_test_pred),
            "test_precision": precision_score(y_test, y_test_pred),
            "test_recall": recall_score(y_test, y_test_pred),
            "test_f1": f1_score(y_test, y_test_pred),
            "test_roc_auc": roc_auc_score(y_test, y_test_proba)
        }
        mlflow.log_metrics(metrics)
        
        # Print results
        print("\n" + "=" * 80)
        print("MODEL PERFORMANCE METRICS")
        print("=" * 80)
        for metric_name, metric_value in metrics.items():
            print(f"   {metric_name:20s}: {metric_value:.4f}")
        
        print("\n" + "-" * 80)
        print("Classification Report:")
        print("-" * 80)
        print(classification_report(y_test, y_test_pred, target_names=['No Default', 'Default']))
        
        print("-" * 80)
        print("Confusion Matrix:")
        print("-" * 80)
        cm = confusion_matrix(y_test, y_test_pred)
        print(f"   True Negatives:  {cm[0, 0]:5d}  |  False Positives: {cm[0, 1]:5d}")
        print(f"   False Negatives: {cm[1, 0]:5d}  |  True Positives:  {cm[1, 1]:5d}")
        
        # Feature importance
        print("\n" + "-" * 80)
        print("Top 10 Most Important Features:")
        print("-" * 80)
        feature_importance = pd.DataFrame({
            'feature': X.columns,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        for idx, row in feature_importance.head(10).iterrows():
            print(f"   {row['feature']:15s}: {row['importance']:.4f}")
        
        # Save feature importance as artifact
        importance_path = "feature_importance.csv"
        feature_importance.to_csv(importance_path, index=False)
        mlflow.log_artifact(importance_path)
        
        # Log model with signature
        print("\n5. Logging model to MLflow...")
        
        # Create model signature
        from mlflow.models import infer_signature
        signature = infer_signature(X_train, y_train_pred)
        
        # Log the sklearn model
        mlflow.sklearn.log_model(
            model,
            "decision_tree_model",
            signature=signature,
            input_example=X_test[:5]
        )
        
        # Also save scaler as artifact
        scaler_path = "scaler.pkl"
        joblib.dump(scaler, scaler_path)
        mlflow.log_artifact(scaler_path)
        
        # Save feature names
        feature_names_path = "feature_names.txt"
        with open(feature_names_path, 'w') as f:
            f.write('\n'.join(X.columns.tolist()))
        mlflow.log_artifact(feature_names_path)
        
        # Get run info
        run_id = mlflow.active_run().info.run_id
        
        print(f"\n   Model logged successfully!")
        print(f"   Run ID: {run_id}")
        print(f"   Artifact URI: {mlflow.get_artifact_uri()}")
        
        print("\n" + "=" * 80)
        print("TRAINING COMPLETE!")
        print("=" * 80)
        print(f"\nTo view results in MLflow UI, run:")
        print(f"   mlflow ui --backend-store-uri file:./mlruns")
        print(f"\nThen open: http://localhost:5000")
        print("=" * 80)
        
        return run_id, model, scaler


if __name__ == "__main__":
    # Train with default parameters
    run_id, model, scaler = train_decision_tree(
        max_depth=10,
        min_samples_split=20,
        min_samples_leaf=10,
        criterion='gini',
        random_state=42
    )
    
    print(f"\n✓ Model training completed. Run ID: {run_id}")
