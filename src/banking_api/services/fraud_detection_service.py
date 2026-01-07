"""Fraud detection service layer.

This module provides business logic for fraud detection and analysis.
"""

from typing import Dict, List
import pandas as pd
from ..models.stats import FraudSummary, FraudByType
from ..models.transaction import FraudPredictionRequest, FraudPredictionResponse
from ..utils.data_loader import DataLoader


class FraudDetectionService:
    """Service for fraud detection operations.

    This service handles fraud analysis and simple fraud prediction.
    """

    def __init__(self) -> None:
        """Initialize the fraud detection service."""
        self.data_loader = DataLoader()

    def get_fraud_summary(self) -> FraudSummary:
        """Get summary of fraud statistics.

        Returns
        -------
        FraudSummary
            Summary including total frauds, flagged count, and fraud rate.
        """
        df = self.data_loader.get_data().copy()

        # Parse amount if needed
        if df['amount'].dtype == 'object':
            df['amount'] = df['amount'].str.replace('$', '').str.replace(',', '').astype(float)

        total_frauds = int(df['isFraud'].sum())
        # No isFlaggedFraud in our dataset, use isFraud as approximation
        flagged = total_frauds
        total_transactions = len(df)
        fraud_rate = total_frauds / total_transactions if total_transactions > 0 else 0

        fraud_df = df[df['isFraud'] == 1]
        total_fraud_amount = float(fraud_df['amount'].sum()) if len(fraud_df) > 0 else 0.0

        return FraudSummary(
            total_frauds=total_frauds,
            flagged=flagged,
            fraud_rate=fraud_rate,
            total_fraud_amount=total_fraud_amount
        )

    def get_fraud_by_type(self) -> List[FraudByType]:
        """Get fraud statistics by transaction method (use_chip).

        Returns
        -------
        List[FraudByType]
            List of fraud statistics for each transaction method.
        """
        df = self.data_loader.get_data()

        fraud_stats = []
        for trans_type in df['use_chip'].dropna().unique():
            type_df = df[df['use_chip'] == trans_type]
            fraud_count = int(type_df['isFraud'].sum())
            total_count = len(type_df)

            fraud_stats.append(FraudByType(
                type=str(trans_type),
                fraud_rate=fraud_count / total_count if total_count > 0 else 0,
                fraud_count=fraud_count,
                total_count=total_count
            ))

        return sorted(fraud_stats, key=lambda x: x.fraud_rate, reverse=True)

    def predict_fraud(
        self,
        request: FraudPredictionRequest
    ) -> FraudPredictionResponse:
        """Predict if a transaction is fraudulent.

        This is a simplified rule-based prediction model.
        In production, this would use a trained ML model.

        Parameters
        ----------
        request : FraudPredictionRequest
            Transaction data for prediction.

        Returns
        -------
        FraudPredictionResponse
            Prediction result with probability.

        Notes
        -----
        This implementation uses simple heuristics:
        - Online/Chip transactions are riskier
        - High amounts are suspicious
        - Certain merchant categories
        - Certain states have higher fraud rates
        """
        score = 0.0

        # Transaction method risk
        if 'Online' in request.use_chip:
            score += 0.3
        elif 'Chip' in request.use_chip:
            score += 0.1

        # High amount risk
        if request.amount > 1000:
            score += 0.3
        if request.amount > 5000:
            score += 0.2

        # Certain MCC codes are riskier (example: 5999 - miscellaneous)
        risky_mcc = [5999, 5815, 5962, 5912]
        if request.mcc in risky_mcc:
            score += 0.2

        # Certain states have higher fraud (example heuristic)
        risky_states = ['CA', 'FL', 'NY', 'TX']
        if request.merchant_state in risky_states:
            score += 0.1

        probability = min(score, 1.0)
        is_fraud = probability > 0.5

        return FraudPredictionResponse(
            isFraud=is_fraud,
            probability=probability
        )
