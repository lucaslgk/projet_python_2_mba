"""Statistics service layer.

This module provides business logic for statistical operations.
"""

from typing import List, Dict, Any
import pandas as pd
import numpy as np
from ..models.stats import (
    StatsOverview,
    AmountDistribution,
    TypeStats,
    DailyStats
)
from ..utils.data_loader import DataLoader


class StatsService:
    """Service for statistical operations.

    This service handles calculation of various statistics
    and aggregations on transaction data.
    """

    def __init__(self) -> None:
        """Initialize the statistics service."""
        self.data_loader = DataLoader()

    def get_overview(self) -> StatsOverview:
        """Get overall statistics of the dataset.

        Returns
        -------
        StatsOverview
            Overall statistics including totals, averages, and fraud rate.
        """
        df = self.data_loader.get_data().copy()

        # Parse amount if needed
        if df['amount'].dtype == 'object':
            df['amount'] = df['amount'].str.replace('$', '').str.replace(',', '').astype(float)

        total_transactions = len(df)
        fraud_count = df['isFraud'].sum()
        fraud_rate = fraud_count / total_transactions if total_transactions > 0 else 0
        avg_amount = float(df['amount'].mean())
        total_amount = float(df['amount'].sum())

        # Most common transaction method instead of type
        most_common_type = df['use_chip'].mode()[0] if len(df) > 0 else "Unknown"

        return StatsOverview(
            total_transactions=total_transactions,
            fraud_rate=fraud_rate,
            avg_amount=avg_amount,
            most_common_type=most_common_type,
            total_amount=total_amount
        )

    def get_amount_distribution(self, num_bins: int = 10) -> AmountDistribution:
        """Get distribution of transaction amounts.

        Parameters
        ----------
        num_bins : int
            Number of bins for the histogram.

        Returns
        -------
        AmountDistribution
            Distribution of amounts across bins.
        """
        df = self.data_loader.get_data().copy()

        # Parse amount if needed
        if df['amount'].dtype == 'object':
            df['amount'] = df['amount'].str.replace('$', '').str.replace(',', '').astype(float)

        counts, bin_edges = np.histogram(df['amount'], bins=num_bins)

        bins = [
            f"{int(bin_edges[i])}-{int(bin_edges[i+1])}"
            for i in range(len(bin_edges) - 1)
        ]

        return AmountDistribution(
            bins=bins,
            counts=counts.tolist()
        )

    def get_stats_by_type(self) -> List[TypeStats]:
        """Get statistics grouped by transaction method (use_chip).

        Returns
        -------
        List[TypeStats]
            List of statistics for each transaction method.
        """
        df = self.data_loader.get_data().copy()

        # Parse amount if needed
        if df['amount'].dtype == 'object':
            df['amount'] = df['amount'].str.replace('$', '').str.replace(',', '').astype(float)

        type_stats = []
        for trans_type in df['use_chip'].dropna().unique():
            type_df = df[df['use_chip'] == trans_type]
            fraud_count = type_df['isFraud'].sum()
            total_count = len(type_df)

            type_stats.append(TypeStats(
                type=str(trans_type),
                count=total_count,
                avg_amount=float(type_df['amount'].mean()),
                total_amount=float(type_df['amount'].sum()),
                fraud_rate=fraud_count / total_count if total_count > 0 else 0
            ))

        return sorted(type_stats, key=lambda x: x.count, reverse=True)

    def get_daily_stats(self) -> List[DailyStats]:
        """Get statistics grouped by date.

        Returns
        -------
        List[DailyStats]
            List of daily statistics.
        """
        df = self.data_loader.get_data().copy()

        # Parse amount if needed
        if df['amount'].dtype == 'object':
            df['amount'] = df['amount'].str.replace('$', '').str.replace(',', '').astype(float)

        # Convert date to datetime and extract date only
        df['date_only'] = pd.to_datetime(df['date']).dt.date

        daily_stats = []
        for date in sorted(df['date_only'].unique()):
            date_df = df[df['date_only'] == date]

            daily_stats.append(DailyStats(
                step=str(date),  # Using date as step
                count=len(date_df),
                avg_amount=float(date_df['amount'].mean()),
                total_amount=float(date_df['amount'].sum()),
                fraud_count=int(date_df['isFraud'].sum())
            ))

        return daily_stats
