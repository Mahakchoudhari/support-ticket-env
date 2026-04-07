import os

print("[START]")

total_score = 0

try:
    import requests
except Exception as e:
    print("Import error:", e)
    exit(1)

BASE_URL = "https://Mahakchoudhari-support-ticket-env.hf.space"

def safe_post(url, **kwargs):
    try:
        res = requests.post(url, timeout=10, **kwargs)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(f"[ERROR] Request failed at {url}:", e)
        return None

for task_id in range(3):

    # Reset environment
    data = safe_post(f"{BASE_URL}/reset", params={"task_id": task_id})
    if not data:
        continue

    obs = data.get("observation", "")
    done = False
    step_num = 0

    while not done:

        if step_num == 0:
            action = {"type": "classify", "content": "billing"}
        elif step_num == 1:
            action = {"type": "act", "content": "refund"}
        else:
            action = {
                "type": "respond",
                "content": "sorry we will help and resolve your issue with refund"
            }

        data = safe_post(f"{BASE_URL}/step", json=action)
        if not data:
            break

        obs = data.get("observation", "")
        reward = data.get("reward", 0)
        done = data.get("done", False)

        print("[STEP] action:", action)
        print("[STEP] reward:", reward)

        step_num += 1

        if step_num > 5:
            break

        if done:
            total_score += reward

print("[END] total_score:", total_score)