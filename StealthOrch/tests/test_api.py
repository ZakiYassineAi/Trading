import requests
import json
import time
import subprocess
import sys
import os

PORT = "8009"
BASE_URL = f"http://0.0.0.0:{PORT}"

def run_all_tests():
    server_process = None
    try:
        print(f"--> Starting server on port {PORT}...")
        command = [
            sys.executable, "-m", "uvicorn",
            "StealthOrch.orchestrator.main:app",
            "--host", "0.0.0.0", "--port", PORT
        ]
        server_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, preexec_fn=os.setsid)
        print("--> Waiting for services to start (5 seconds)...")
        time.sleep(5)

        print("\n--- Running E2E Test: Full Safe Mode Flow ---")
        test_full_safe_flow()

        print("\n--- Running Test: Dashboard UI ---")
        test_dashboard_ui()

        print("\n\n--- ✅ All Tests Passed! ---")

    finally:
        if server_process:
            print("\n--> Terminating server subprocess...")
            os.killpg(os.getpgid(server_process.pid), subprocess.signal.SIGTERM)
            stdout, stderr = server_process.communicate()
            print("\n--- Server STDOUT ---")
            print(stdout)
            print("\n--- Server STDERR ---")
            print(stderr)

def create_test_opportunity(project_name: str):
    # ... (omitted for brevity, same as before)
    payload = {"project": project_name, "contract_address": "0x779877A7B0D9E8603169DdbD7836e478b4624789", "function_name": "claim", "args": {"recipient": "0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B", "amount": 10**18}, "chain": "SEPOLIA", "priority": 5}
    response = requests.post(f"{BASE_URL}/opportunities", json=payload)
    response.raise_for_status()
    return response.json()

def test_full_safe_flow():
    # ... (omitted for brevity, same as before)
    print("1. Creating opportunity for safe mode...")
    opp = create_test_opportunity("TestE2ESafeFlow_UI")
    opp_id = opp['id']
    print(f"   ✅ Opportunity created with ID: {opp_id}")

    print("2. Preparing transaction with mode=safe...")
    res = requests.post(f"{BASE_URL}/prepare/{opp_id}?mode=safe")
    assert res.status_code == 200, f"Prepare failed: {res.text}"
    print(f"   ✅ Transaction prepared successfully.")

def test_dashboard_ui():
    print("1. Fetching dashboard HTML...")
    res = requests.get(BASE_URL + "/")
    assert res.status_code == 200
    html = res.text
    print("   ✅ Dashboard is accessible.")
    print(f"--- Received HTML ---\n{html}\n---------------------")

    print("2. Verifying content...")
    # Check that the opportunity we created in the previous test is rendered
    assert "TestE2ESafeFlow_UI" in html
    assert "<td>safe</td>" in html
    assert "Submit to Safe" in html
    print("   ✅ Prepared transaction data is correctly rendered in the UI.")


if __name__ == "__main__":
    run_all_tests()
