"""
Test script for the Credit Default API
"""
import requests
import json


def test_health_check():
    """Test the health endpoint"""
    print("=" * 80)
    print("Testing Health Check Endpoint")
    print("=" * 80)
    
    url = "http://localhost:3033/health"
    response = requests.post(url)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()
    
    return response.status_code == 200


def test_single_prediction():
    """Test single prediction"""
    print("=" * 80)
    print("Testing Single Prediction Endpoint")
    print("=" * 80)
    
    url = "http://localhost:3033/predict"
    
    # Example application - low risk profile
    data = {
        "LIMIT_BAL": 200000,
        "SEX": 2,
        "EDUCATION": 2,
        "MARRIAGE": 1,
        "AGE": 35,
        "PAY_0": 0,
        "PAY_2": 0,
        "PAY_3": 0,
        "PAY_4": 0,
        "PAY_5": 0,
        "PAY_6": 0,
        "BILL_AMT1": 15000,
        "BILL_AMT2": 14000,
        "BILL_AMT3": 13000,
        "BILL_AMT4": 12000,
        "BILL_AMT5": 11000,
        "BILL_AMT6": 10000,
        "PAY_AMT1": 2000,
        "PAY_AMT2": 2000,
        "PAY_AMT3": 2000,
        "PAY_AMT4": 2000,
        "PAY_AMT5": 2000,
        "PAY_AMT6": 2000
    }
    
    print("Input data (Low Risk Profile):")
    print(json.dumps(data, indent=2))
    print()
    
    response = requests.post(url, json=data)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()
    
    return response.status_code == 200


def test_high_risk_prediction():
    """Test prediction with high risk profile"""
    print("=" * 80)
    print("Testing High Risk Prediction")
    print("=" * 80)
    
    url = "http://localhost:3033/predict"
    
    # Example application - high risk profile
    data = {
        "LIMIT_BAL": 50000,
        "SEX": 1,
        "EDUCATION": 3,
        "MARRIAGE": 2,
        "AGE": 24,
        "PAY_0": 3,
        "PAY_2": 3,
        "PAY_3": 2,
        "PAY_4": 2,
        "PAY_5": 1,
        "PAY_6": 1,
        "BILL_AMT1": 45000,
        "BILL_AMT2": 44000,
        "BILL_AMT3": 43000,
        "BILL_AMT4": 42000,
        "BILL_AMT5": 41000,
        "BILL_AMT6": 40000,
        "PAY_AMT1": 500,
        "PAY_AMT2": 500,
        "PAY_AMT3": 500,
        "PAY_AMT4": 500,
        "PAY_AMT5": 500,
        "PAY_AMT6": 500
    }
    
    print("Input data (High Risk Profile):")
    print(json.dumps(data, indent=2))
    print()
    
    response = requests.post(url, json=data)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()
    
    return response.status_code == 200


def test_batch_prediction():
    """Test batch prediction"""
    print("=" * 80)
    print("Testing Batch Prediction Endpoint")
    print("=" * 80)
    
    url = "http://localhost:3033/predict_batch"
    
    data = [
        {
            "LIMIT_BAL": 200000, "SEX": 2, "EDUCATION": 2, "MARRIAGE": 1, "AGE": 35,
            "PAY_0": 0, "PAY_2": 0, "PAY_3": 0, "PAY_4": 0, "PAY_5": 0, "PAY_6": 0,
            "BILL_AMT1": 15000, "BILL_AMT2": 14000, "BILL_AMT3": 13000,
            "BILL_AMT4": 12000, "BILL_AMT5": 11000, "BILL_AMT6": 10000,
            "PAY_AMT1": 2000, "PAY_AMT2": 2000, "PAY_AMT3": 2000,
            "PAY_AMT4": 2000, "PAY_AMT5": 2000, "PAY_AMT6": 2000
        },
        {
            "LIMIT_BAL": 50000, "SEX": 1, "EDUCATION": 3, "MARRIAGE": 2, "AGE": 24,
            "PAY_0": 3, "PAY_2": 3, "PAY_3": 2, "PAY_4": 2, "PAY_5": 1, "PAY_6": 1,
            "BILL_AMT1": 45000, "BILL_AMT2": 44000, "BILL_AMT3": 43000,
            "BILL_AMT4": 42000, "BILL_AMT5": 41000, "BILL_AMT6": 40000,
            "PAY_AMT1": 500, "PAY_AMT2": 500, "PAY_AMT3": 500,
            "PAY_AMT4": 500, "PAY_AMT5": 500, "PAY_AMT6": 500
        }
    ]
    
    print(f"Sending {len(data)} applications for batch prediction...")
    print()
    
    response = requests.post(url, json=data)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()
    
    return response.status_code == 200


def test_feature_importance():
    """Test feature importance endpoint"""
    print("=" * 80)
    print("Testing Feature Importance Endpoint")
    print("=" * 80)
    
    url = "http://localhost:3033/feature_importance"
    response = requests.post(url)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        importance = response.json()
        print("\nTop 10 Most Important Features:")
        print("-" * 80)
        for i, (feature, score) in enumerate(list(importance.items())[:10], 1):
            print(f"{i:2d}. {feature:15s}: {score:.4f}")
    else:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    print()
    return response.status_code == 200


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("CREDIT DEFAULT API - TEST SUITE")
    print("=" * 80)
    print()
    
    tests = [
        ("Health Check", test_health_check),
        ("Single Prediction (Low Risk)", test_single_prediction),
        ("Single Prediction (High Risk)", test_high_risk_prediction),
        ("Batch Prediction", test_batch_prediction),
        ("Feature Importance", test_feature_importance),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, "✓ PASSED" if success else "✗ FAILED"))
        except Exception as e:
            print(f"Error: {e}\n")
            results.append((test_name, f"✗ ERROR: {str(e)}"))
    
    print("=" * 80)
    print("TEST RESULTS SUMMARY")
    print("=" * 80)
    for test_name, result in results:
        print(f"{test_name:40s}: {result}")
    print("=" * 80)
