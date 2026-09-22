"""Extracts supplementary data (e.g. currency rates) from a public REST API."""

import os
import requests
import pandas as pd


def extract_api(endpoint_env_var: str = "API_BASE_URL", timeout: int = 10) -> pd.DataFrame:
    """
    Call a REST API and return the response as a flat DataFrame.

    Falls back to an empty DataFrame (with a logged reason upstream) if the
    API is unreachable — the pipeline should not hard-fail on an optional
    enrichment source.

    Args:
        endpoint_env_var: Environment variable name holding the API base URL.
        timeout: Request timeout in seconds.

    Returns:
        DataFrame built from the API's JSON response.
    """
    url = os.getenv(endpoint_env_var, "")
    if not url:
        return pd.DataFrame()

    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    payload = response.json()

    # Normalize a nested "rates" dict (exchangerate.host-style response)
    # into a two-column DataFrame; adjust to your actual API's shape.
    if isinstance(payload, dict) and "rates" in payload:
        rates = payload["rates"]
        return pd.DataFrame(list(rates.items()), columns=["currency", "rate"])

    return pd.json_normalize(payload)
