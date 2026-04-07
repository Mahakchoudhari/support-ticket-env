from fastapi import FastAPI, Request
from support_env import SupportEnv
import uvicorn

app = FastAPI()
env = SupportEnv()

@app.get("/")
def root():
    return {"message": "API is running"}

@app.post("/reset")
async def reset(request: Request):
    try:
        data = await request.json()
        task_id = data.get("task_id", 0)
    except:
        task_id = 0

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


def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()