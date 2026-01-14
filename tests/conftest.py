"""Pytest configuration and fixtures.

This module provides shared fixtures for testing.
"""

import pytest
import pandas as pd
from fastapi.testclient import TestClient
from src.banking_api.app import create_app
from src.banking_api.utils.data_loader import DataLoader


@pytest.fixture(scope="session")
def sample_data() -> pd.DataFrame:
    """Create sample transaction data for testing.

    Returns
    -------
    pd.DataFrame
        Sample transaction data.
    """
    data = {
        'step': [1, 1, 2, 2, 3],
        'type': ['PAYMENT', 'TRANSFER', 'CASH_OUT', 'PAYMENT', 'TRANSFER'],
        'amount': [9839.64, 181.0, 181.0, 1000.0, 5000.0],
        'nameOrig': ['C1231006815', 'C1666544295', 'C1305486145',
                     'C1231006815', 'C1666544295'],
        'oldbalanceOrg': [170136.0, 181.0, 181.0, 170136.0, 5000.0],
        'newbalanceOrig': [160296.36, 0.0, 0.0, 169136.0, 0.0],
        'nameDest': ['M1979787155', 'C1900366749', 'C840083671',
                     'M1979787155', 'C1900366749'],
        'oldbalanceDest': [0.0, 0.0, 0.0, 0.0, 0.0],
        'newbalanceDest': [0.0, 0.0, 0.0, 0.0, 5000.0],
        'isFraud': [0, 1, 1, 0, 0],
        'isFlaggedFraud': [0, 0, 0, 0, 0]
    }
    df = pd.DataFrame(data)
    df['id'] = df.index.map(lambda x: f"tx_{x:07d}")
    return df


@pytest.fixture(scope="session")
def load_sample_data(sample_data: pd.DataFrame) -> None:
    """Load sample data into DataLoader.

    Parameters
    ----------
    sample_data : pd.DataFrame
        Sample transaction data.
    """
    loader = DataLoader()
    loader._data = sample_data


@pytest.fixture
def client(load_sample_data: None) -> TestClient:
    """Create test client.

    Parameters
    ----------
    load_sample_data : None
        Fixture to ensure data is loaded.

    Returns
    -------
    TestClient
        FastAPI test client.
    """
    app = create_app()
    return TestClient(app)
