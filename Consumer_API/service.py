"""
BentoML service for Credit Card Default prediction
"""
import bentoml
import numpy as np
import pandas as pd
from pydantic import BaseModel, Field
from typing import List, Dict, Any
import mlflow
import joblib
import os


# Define input schema
class CreditApplication(BaseModel):
    """Input schema for credit card application"""
    LIMIT_BAL: float = Field(description="Credit limit", ge=0)
    SEX: int = Field(description="Gender (1=male, 2=female)", ge=1, le=2)
    EDUCATION: int = Field(description="Education (1=graduate, 2=university, 3=high school, 4=others)", ge=1, le=4)
    MARRIAGE: int = Field(description="Marital status (1=married, 2=single, 3=others)", ge=1, le=3)
    AGE: int = Field(description="Age in years", ge=18, le=100)
    PAY_0: int = Field(description="Repayment status in September", ge=-2, le=8)
    PAY_2: int = Field(description="Repayment status in August", ge=-2, le=8)
    PAY_3: int = Field(description="Repayment status in July", ge=-2, le=8)
    PAY_4: int = Field(description="Repayment status in June", ge=-2, le=8)
    PAY_5: int = Field(description="Repayment status in May", ge=-2, le=8)
    PAY_6: int = Field(description="Repayment status in April", ge=-2, le=8)
    BILL_AMT1: float = Field(description="Bill statement in September", ge=0)
    BILL_AMT2: float = Field(description="Bill statement in August", ge=0)
    BILL_AMT3: float = Field(description="Bill statement in July", ge=0)
    BILL_AMT4: float = Field(description="Bill statement in June", ge=0)
    BILL_AMT5: float = Field(description="Bill statement in May", ge=0)
    BILL_AMT6: float = Field(description="Bill statement in April", ge=0)
    PAY_AMT1: float = Field(description="Payment in September", ge=0)
    PAY_AMT2: float = Field(description="Payment in August", ge=0)
    PAY_AMT3: float = Field(description="Payment in July", ge=0)
    PAY_AMT4: float = Field(description="Payment in June", ge=0)
    PAY_AMT5: float = Field(description="Payment in May", ge=0)
    PAY_AMT6: float = Field(description="Payment in April", ge=0)


class PredictionResponse(BaseModel):
    """Output schema for prediction"""
    prediction: int = Field(description="Predicted class (0=no default, 1=default)")
    probability: float = Field(description="Probability of default")
    risk_level: str = Field(description="Risk assessment (low/medium/high)")


# Load the model from MLflow
def load_model_from_mlflow():
    """Load the latest model from MLflow"""
    mlflow.set_tracking_uri("file:./mlruns")
    
    # Get the latest run from the experiment
    experiment = mlflow.get_experiment_by_name("credit_default_prediction")
    if experiment is None:
        raise ValueError("No experiment found. Please train a model first using train.py")
    
    runs = mlflow.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=["start_time DESC"],
        max_results=1
    )
    
    if runs.empty:
        raise ValueError("No runs found. Please train a model first using train.py")
    
    run_id = runs.iloc[0].run_id
    
    # Load model
    model_uri = f"runs:/{run_id}/decision_tree_model"
    model = mlflow.sklearn.load_model(model_uri)
    
    # Load scaler
    client = mlflow.tracking.MlflowClient()
    scaler_path = client.download_artifacts(run_id, "scaler.pkl")
    scaler = joblib.load(scaler_path)
    
    # Load feature names
    feature_names_path = client.download_artifacts(run_id, "feature_names.txt")
    with open(feature_names_path, 'r') as f:
        feature_names = [line.strip() for line in f.readlines()]
    
    print(f"✓ Model loaded from run: {run_id}")
    return model, scaler, feature_names


# Initialize model and scaler
try:
    MODEL, SCALER, FEATURE_NAMES = load_model_from_mlflow()
except Exception as e:
    print(f"Warning: Could not load model from MLflow: {e}")
    print("Please run train.py first to train and save a model.")
    MODEL, SCALER, FEATURE_NAMES = None, None, None


# Create BentoML service
@bentoml.service(
    name="credit_default_classifier",
    resources={
        "cpu": "2",
        "memory": "2Gi",
    },
)
class CreditDefaultService:
    """BentoML service for credit card default prediction"""
    
    def __init__(self):
        self.model = MODEL
        self.scaler = SCALER
        self.feature_names = FEATURE_NAMES
    
    @bentoml.api
    def predict(self, application: CreditApplication) -> PredictionResponse:
        """
        Predict credit card default probability.
        
        Args:
            application: Credit application data
            
        Returns:
            Prediction with probability and risk level
        """
        if self.model is None:
            raise ValueError("Model not loaded. Please train a model first using train.py")
        
        # Convert input to DataFrame
        input_dict = application.model_dump()
        input_df = pd.DataFrame([input_dict])
        
        # Ensure correct column order
        input_df = input_df[self.feature_names]
        
        # Scale features
        input_scaled = self.scaler.transform(input_df)
        
        # Make prediction
        prediction = int(self.model.predict(input_scaled)[0])
        probability = float(self.model.predict_proba(input_scaled)[0, 1])
        
        # Determine risk level
        if probability < 0.3:
            risk_level = "low"
        elif probability < 0.7:
            risk_level = "medium"
        else:
            risk_level = "high"
        
        return PredictionResponse(
            prediction=prediction,
            probability=probability,
            risk_level=risk_level
        )
    
    @bentoml.api
    def predict_batch(self, applications: List[CreditApplication]) -> List[PredictionResponse]:
        """
        Batch prediction for multiple applications.
        
        Args:
            applications: List of credit applications
            
        Returns:
            List of predictions
        """
        if self.model is None:
            raise ValueError("Model not loaded. Please train a model first using train.py")
        
        # Convert to DataFrame
        input_dicts = [app.model_dump() for app in applications]
        input_df = pd.DataFrame(input_dicts)
        
        # Ensure correct column order
        input_df = input_df[self.feature_names]
        
        # Scale features
        input_scaled = self.scaler.transform(input_df)
        
        # Make predictions
        predictions = self.model.predict(input_scaled)
        probabilities = self.model.predict_proba(input_scaled)[:, 1]
        
        # Build responses
        responses = []
        for pred, prob in zip(predictions, probabilities):
            if prob < 0.3:
                risk_level = "low"
            elif prob < 0.7:
                risk_level = "medium"
            else:
                risk_level = "high"
            
            responses.append(PredictionResponse(
                prediction=int(pred),
                probability=float(prob),
                risk_level=risk_level
            ))
        
        return responses
    
    @bentoml.api
    def health(self) -> Dict[str, Any]:
        """
        Health check endpoint.
        
        Returns:
            Service health status
        """
        return {
            "status": "healthy",
            "model_loaded": self.model is not None,
            "scaler_loaded": self.scaler is not None,
            "n_features": len(self.feature_names) if self.feature_names else 0
        }
    
    @bentoml.api
    def feature_importance(self) -> Dict[str, float]:
        """
        Get feature importance from the model.
        
        Returns:
            Dictionary of feature names and their importance scores
        """
        if self.model is None:
            raise ValueError("Model not loaded")
        
        importance_dict = {}
        for feature, importance in zip(self.feature_names, self.model.feature_importances_):
            importance_dict[feature] = float(importance)
        
        # Sort by importance
        importance_dict = dict(sorted(importance_dict.items(), key=lambda x: x[1], reverse=True))
        
        return importance_dict
