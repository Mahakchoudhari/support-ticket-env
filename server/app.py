from fastapi import FastAPI
from support_env import SupportEnv

app = FastAPI()
env = SupportEnv()

@app.post("/reset")
def reset(task_id: int = 0):
    obs = env.reset(task_id)
    return {"observation": obs}

@app.post("/step")
def step(action: dict):
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": info
    }

@app.get("/state")
def state():
    return env.state()