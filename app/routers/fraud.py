from fastapi import APIRouter, Depends, HTTPException, Depends  # type: ignore
from datetime import datetime 
import pandas as pd
from typing import List, Dict, Any

from app.models.schemas import TransactionRequest, PredictionResponse, ModelInfoResponse, ModelMetricsResponse
from app.services.fraud_services import FraudDetectionService
from app.services.metrics_service import MetricsService

router = APIRouter(prefix="/fraud", tags=["fraud"], 
                   responses={404: {"description": "Not Found"}})

# Initialize the fraud detection service
def get_fraud_service():
    return FraudDetectionService()

@router.post("/predict", response_model=PredictionResponse)
def predict_fraud(request: TransactionRequest,
                        service: FraudDetectionService = Depends(get_fraud_service)):
    """
    Predict if a transaction is fraudulent.
    Args:
        request: Transaction data as TransactionRequest
        service: FraudDetectionService instance
    Returns:
        PredictionResponse containing fraud prediction details
    """

    try: 
        # Convert request data into DataFrame
        data = pd.DataFrame([{
            "transaction_amount": request.transaction_amount,
            "is_nighttime": request.is_nighttime,
            "category": request.category,
            "transaction_location": request.transaction_location,
            "job": request.job,
            "state": request.state,
            "transaction_number": request.transaction_number
        }])

        # Make prediction 
        is_fraud, label, fraud_probability = service.predict(data)

        # Create response object
        response = PredictionResponse(
            transaction_id=request.transaction_number,
            is_fraud=is_fraud,
            label=label,
            fraud_probability=fraud_probability,
            timestamp=datetime.now()
        )

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/model_info", response_model=ModelInfoResponse)
def get_model_info(service: FraudDetectionService = Depends(get_fraud_service)):
    """
    Get information about the fraud detection model.
    Args:
        service: FraudDetectionService instance
    Returns:
        ModelInfoResponse containing model details
    """
    try:
        info = service.get_model_info()
        return info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Add dependency for MetricsService
def get_metrics_service():
    service = MetricsService()
    try:
        yield service
    finally:
        service.close()

@router.get("/metrics", response_model=ModelMetricsResponse)
def get_model_metrics(model_version: str = "1.0.0",
                            service: MetricsService = Depends(get_metrics_service)):
    """
    Get model performance metrics.
    Args:
        model_version: Version of the model to retrieve metrics for
        service: MetricsService instance
    Returns:
        ModelMetricsResponse containing model performance metrics
    """
    try:
        metrics = service.get_model_metrics(model_version)
        if not metrics:
            raise HTTPException(status_code=404, detail="Metrics not found")
        return metrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))