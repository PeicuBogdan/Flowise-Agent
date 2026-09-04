import requests
from config import FLOWISE_URL, FLOW_ID, API_KEY

def ask(question: str, timeout: int = 180) -> dict:
    response = requests.post(
        f"{FLOWISE_URL}/api/v1/prediction/{FLOW_ID}",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"question": question},
        timeout=timeout,
    )
    response.raise_for_status()
    return response.json()