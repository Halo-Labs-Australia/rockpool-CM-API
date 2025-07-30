import os
import base64
import requests
import pandas as pd

BASE_URL = "https://rockpoolrac.residential.icarehealth.com.au/Tetra.Web"
TOKEN_URL = f"{BASE_URL}/OAuth/Token"
API_USER = "cmapi"

def get_cm_access_token() -> str:
    """
    Obtain an OAuth2 access token using client credentials flow.
    Requires the CM_API_PASSWORD to be set in the environment.
    """
    password = os.getenv("CM_API_PASSWORD")
    if not password:
        raise EnvironmentError("CM_API_PASSWORD not set in environment.")

    # Construct Basic Auth header
    credentials = f"{API_USER}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {"grant_type": "client_credentials"}

    response = requests.post(TOKEN_URL, headers=headers, data=data)
    if response.ok:
        return response.json().get("access_token")
    else:
        raise requests.HTTPError(
            f"Failed to get token: {response.status_code} - {response.text}"
        )


def get_residency(facility_id: int, token: str) -> pd.DataFrame:
    """
    Fetch residency data for a given facility ID and return as a DataFrame.
    """
    url = f"{BASE_URL}/api/ExternalResidencyV2/Search?facilityId={facility_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers)
    if not response.ok:
        raise requests.HTTPError(
            f"Failed to fetch residency for facility {facility_id}: "
            f"{response.status_code} - {response.text}"
        )

    data = response.json().get("Residencies", [])
    return pd.DataFrame(data)
