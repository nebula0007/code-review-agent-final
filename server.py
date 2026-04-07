from fastapi import FastAPI, HTTPException
from app.env import CodeReviewEnv
from app.models import Action

app = FastAPI()

env = CodeReviewEnv()


# ✅ Root (fixes empty HuggingFace page)
@app.get("/")
def root():
    return {"message": "Code Review Env is running"}


# 🔁 Reset
@app.post("/reset")
def reset():
    obs = env.reset()

    return {
        "observation": obs.dict(),
        "reward": 0.0,
        "done": False,
        "info": {}
    }


# ▶️ Step
@app.post("/step")
def step(action: Action):
    try:
        if env.current_task is None:
            raise HTTPException(status_code=400, detail="Call /reset first")

        result = env.step(action)

        return {
            "observation": result.observation.dict(),
            "reward": result.reward,
            "done": result.done,
            "info": result.info
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 📊 State
@app.get("/state")
def state():
    return env.state()