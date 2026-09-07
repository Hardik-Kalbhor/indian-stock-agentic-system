import json

with open("pipeline_out.json") as f:
    context = json.load(f)

payload = {
    "messages": [{"role": "user", "content": "how much time it will take to reach the base case?"}],
    "context_data": context
}

with open("chat_payload.json", "w") as f:
    json.dump(payload, f)
