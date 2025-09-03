import requests

BASE_URL = "http://0.0.0.0:8008"

def create_opportunity(project_name: str):
    payload = {
        "project": project_name,
        "contract_address": "0x779877A7B0D9E8603169DdbD7836e478b4624789",
        "function_name": "claim",
        "args": {"recipient": "0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B", "amount": 10**18},
        "chain": "SEPOLIA", "priority": 5
    }
    response = requests.post(f"{BASE_URL}/opportunities", json=payload)
    response.raise_for_status()
    return response.json()

def main():
    print("Populating database with prepared transactions...")

    # Create and prepare a 'safe' mode transaction
    opp_safe = create_opportunity("UIPopulate_Safe")
    requests.post(f"{BASE_URL}/prepare/{opp_safe['id']}?mode=safe")
    print(f"  - Prepared 'safe' tx for opportunity {opp_safe['id']}")

    # Create and prepare a 'relayer' mode transaction
    opp_relayer = create_opportunity("UIPopulate_Relayer")
    requests.post(f"{BASE_URL}/prepare/{opp_relayer['id']}?mode=relayer")
    print(f"  - Prepared 'relayer' tx for opportunity {opp_relayer['id']}")

    print("Database populated.")

if __name__ == "__main__":
    main()
