import requests
import base64
import os

def get_cm_access_token():
    # Credentials
    password = os.getenv("CM_API_PASSWORD", "")  # Default value for testing
    username = "cmapi"
    # Token URL
    token_url = "https://rockpoolrac.residential.icarehealth.com.au/Tetra.Web/OAuth/Token"
    # Encode Basic Auth header
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
    # Headers and form data
    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials"
    }
    # Token request
    response = requests.post(token_url, headers=headers, data=data)
    if response.status_code == 200:
        token = response.json().get("access_token")
        return token
    else:
        raise Exception(f"Failed to retrieve token: {response.status_code} - {response.text}")

    
def get_residency(facility_id, TOKEN):
    url = f"{BASE_URL}/api/ExternalResidencyV2/Search?facilityId={facility_id}"
    
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Will raise an error for 401, 403, etc.

    if response.status_code != 200:
        raise Exception(f"Failed to retrieve data: {response.status_code} - {response.text}")
    
    data = response.json()["Residencies"]

    # If the data is nested, adjust this line as needed
    df = pd.DataFrame(data)
    return df