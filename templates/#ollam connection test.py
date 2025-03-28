#ollam connection test.py
import requests
import json

# Ollama API endpoint
OLLAMA_URL = "http://localhost:11434/api/generate"

# Define the request payload
payload = {
    "model": "llama3.2",
    "prompt": "Why is the sky blue?",  # Change the prompt as needed
    "stream": False  # Set to True for streaming response
}

# Define headers
headers = {"Content-Type": "application/json"}

# Send the request to Ollama
try:
    response = requests.post(OLLAMA_URL, headers=headers, data=json.dumps(payload))
    
    # Check if the request was successful
    if response.status_code == 200:
        result = response.json()
        print("\n🟢 Response from Ollama (llama3.2):")
        print(result["response"])
    else:
        print("\n🔴 Error:", response.status_code, response.text)

except requests.exceptions.ConnectionError:
    print("\n❌ Could not connect to Ollama. Make sure the server is running.")
