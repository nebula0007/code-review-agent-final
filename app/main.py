from fastapi import FastAPI
from app.env import CodeReviewEnv
from app.models import Action
from fastapi import HTTPException

app = FastAPI()
env = CodeReviewEnv()


@app.post("/reset")
def reset():
    obs = env.reset()
    return {
        "observation": obs.dict(),
        "reward": 0.0,
        "done": False,
        "info": {}
    }


@app.post("/step")
def step(action: Action):
    try:
        result = env.step(action)
        return {
            "observation": result.observation.dict(),
            "reward": result.reward,
            "done": result.done,
            "info": result.info
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/state")
def state():
    return env.state()


def main():
    return app