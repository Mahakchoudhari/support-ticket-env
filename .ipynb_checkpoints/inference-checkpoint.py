from support_env import SupportEnv

env = SupportEnv()

print("[START]")

total_score = 0

# Loop through all 3 tasks
for i in range(3):
    obs = env.reset(i)
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

        # Take step in environment
        obs, reward, done, _ = env.step(action)

        # Required logs
        print("[STEP] action:", action)
        print("[STEP] reward:", reward)

        step_num += 1

        # Safety break (VERY IMPORTANT)
        if step_num > 5:
            print("[STEP] forced stop")
            break

        if done:
            total_score += reward

print("[END] total_score:", total_score)