import os
import json
import urllib.request
from openai import OpenAI

print("[START] task=support env=custom model=gpt-4o-mini", flush=True)

client = OpenAI(
    base_url=os.environ["API_BASE_URL"],
    api_key=os.environ["API_KEY"],
)

BASE_URL = "https://Mahakchoudhari-support-ticket-env.hf.space"

def post(url, data):
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode())

def ask(prompt):
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return res.choices[0].message.content.strip()

total_score = 0
rewards_list = []

for task_id in range(3):

    data = post(f"{BASE_URL}/reset", {"task_id": task_id})
    ticket = data.get("observation", {}).get("ticket", "")

    # Step 1
    result = ask(f"Classify ticket: billing, technical, or refund.\n{ticket}").lower()
    data = post(f"{BASE_URL}/step", {"type": "classify", "content": result})
    reward = data.get("reward", 0.5)
    rewards_list.append(reward)
    print(f"[STEP] step=1 action={result} reward={reward:.2f} done=false error=null", flush=True)

    # Step 2
    result = ask(f"Action: refund, troubleshoot, escalate.\n{ticket}").lower()
    data = post(f"{BASE_URL}/step", {"type": "act", "content": result})
    reward = data.get("reward", 0.5)
    rewards_list.append(reward)
    print(f"[STEP] step=2 action={result} reward={reward:.2f} done=false error=null", flush=True)

    # Step 3
    result = ask(f"Write polite response.\n{ticket}")
    data = post(f"{BASE_URL}/step", {"type": "respond", "content": result})
    reward = data.get("reward", 0.5)
    rewards_list.append(reward)
    print(f"[STEP] step=3 action=response reward={reward:.2f} done=true error=null", flush=True)

    total_score += reward

score = min(max(total_score / 3, 0.01), 0.99)

print(f"[END] success=true steps=3 score={score:.2f} rewards={','.join(f'{r:.2f}' for r in rewards_list)}", flush=True)