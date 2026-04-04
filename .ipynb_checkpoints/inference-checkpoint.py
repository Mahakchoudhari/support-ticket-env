import requests
import os


BASE_URL = "https://Mahakchoudhari-support-ticket-env.hf.space"
print("[START]")

total_score = 0

for task_id in range(3):

    # Reset environment
    res = requests.post(f"{BASE_URL}/reset", params={"task_id": task_id})
    obs = res.json()["observation"]

    done = False
    step_num = 0

    while not done:

        # Simple rule-based logic
        if step_num == 0:
            action = {"type": "classify", "content": "billing"}

        elif step_num == 1:
            action = {"type": "act", "content": "refund"}

        else:
            action = {
                "type": "respond",
                "content": "sorry we will help and resolve your issue with refund"
            }

        # Send action
        res = requests.post(f"{BASE_URL}/step", json=action)
        data = res.json()

        obs = data["observation"]
        reward = data["reward"]
        done = data["done"]

        print("[STEP] action:", action)
        print("[STEP] reward:", reward)

        step_num += 1

        if step_num > 5:
            break

        if done:
            total_score += reward

print("[END] total_score:", total_score)