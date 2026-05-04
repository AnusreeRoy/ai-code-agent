# demo.py

import requests
import json

API_URL = "http://127.0.0.1:8000/run_agent"

def run_demo():
    print("🚀 Running AI Agent Demo...\n")

    # Example: Buggy code/ user input
    payload = {
        "goal": "Fix, analyze and run test",
        "language": "python",
        "code": """
    def main():
    a = 5
    b = 0
    c = a / b
        """
    }

    print("📥 Input Code:\n", payload["code"])

    response = requests.post(API_URL, json=payload)

    if response.status_code != 200:
        print("❌ API Error:", response.text)
        return

    data = response.json()
    print("\n🔍 FULL RESPONSE:")
    print(json.dumps(data, indent=2))

    print("\n🧠 PLAN:")
    for step in data["plan"]:
        print(" -", step)

    print("\n🔧 FINAL CODE:\n")
    print(data["final_code"])

    print("\n🧪 TESTS:\n")
    print(data["tests"])

    print("\n📊 ANALYSIS:\n")
    print(data.get("analysis", ""))

    print("\n📌 OBSERVATIONS:")
    for obs in data["result"]["observations"]:
        print(f"\nStep: {obs['step']}")
        print(f"Tool: {obs['tool']}")
        print(f"Confidence: {obs.get('confidence', 'N/A')}")
        print("\n📌 OBSERVATIONS:")
        result = obs.get("result")
    
        if isinstance(result, str):
            preview = result[:200]
        elif isinstance(result, dict):
            preview = json.dumps(result, indent=2)[:200]
        else:
            preview = str(result)[:200]
    
        print("Result preview:", preview, "...")

    print("\n📖 EXPLANATION:\n")
    print(data["result"]["explanation"])

    print("\n✅ Demo Complete!")

if __name__ == "__main__":
    run_demo()