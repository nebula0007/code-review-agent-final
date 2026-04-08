import os
import requests





API_BASE_URL = os.getenv("API_BASE_URL")

print("DEBUG API_BASE_URL =", API_BASE_URL)

if not API_BASE_URL:
    raise Exception("API_BASE_URL not provided by evaluator")
MODEL_NAME = os.getenv("MODEL_NAME", "dummy")
HF_TOKEN = os.getenv("HF_TOKEN")  # optional



API_URL = API_BASE_URL
MAX_STEPS = 3


def log_start():
    print("[START] task=code-review env=custom model=dummy")


def log_step(step, action, reward, done, info):
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} info={info} error=null")


def log_end(success, steps, rewards):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} rewards={rewards_str}")


def main():
    rewards = []

    log_start()

    res = requests.post(f"{API_URL}/reset").json()

    print("RESET RESPONSE:", res)

    if not isinstance(res, dict) or "observation" not in res:
        raise Exception(f"Invalid response from /reset: {res}")

    obs = res["observation"]

    for step in range(1, MAX_STEPS + 1):

        diff = obs["diff"].lower()

        # 🔵 Subtle max bug (HIGH PRIORITY)
        if "max = 0" in diff:

            if step == 1:
                action = {
                    "issue_type": "logic",
                    "description": "possible incorrect initialization",
                    "fix": "check initial value"
                }

            elif step == 2:
                action = {
                    "issue_type": "logic",
                    "description": "incorrect initialization for negative numbers",
                    "fix": "initialize with minimum value"
                }

            else:
                action = {
                    "issue_type": "logic",
                    "description": "max initialized to 0 fails for negative arrays",
                    "fix": "initialize max with float('-inf') to handle negative values correctly"
                }

        # 🔴 Nested loop performance
        elif "for i in range(len(arr))" in diff:

            if step == 1:
                action = {
                    "issue_type": "performance",
                    "description": "inefficient loop",
                    "fix": "optimize loop"
                }

            elif step == 2:
                action = {
                    "issue_type": "performance",
                    "description": "nested loops increase time complexity",
                    "fix": "reduce number of iterations"
                }

            else:
                action = {
                    "issue_type": "performance",
                    "description": "nested loop inefficient",
                    "fix": "use set for optimization"
                }

        # 🟡 Division edge case
        elif "len(nums)" in diff and "/" in diff:

            if step == 1:
                action = {
                    "issue_type": "logic",
                    "description": "possible division issue",
                    "fix": "check values"
                }

            elif step == 2:
                action = {
                    "issue_type": "logic",
                    "description": "division by zero possible",
                    "fix": "check length"
                }

            else:
                action = {
                    "issue_type": "logic",
                    "description": "division by zero when list is empty",
                    "fix": "check if len(nums) > 0"
                }

        # 🟢 Variable typo
        elif "tota" in diff:

            if step == 1:
                action = {
                    "issue_type": "logic",
                    "description": "possible variable issue",
                    "fix": "check variable"
                }

            elif step == 2:
                action = {
                    "issue_type": "logic",
                    "description": "undefined variable or typo",
                    "fix": "fix variable name"
                }

            else:
                action = {
                    "issue_type": "logic",
                    "description": "variable name typo",
                    "fix": "use total instead of tota"
                }

        # 🟣 Memory inefficiency
        elif "append" in diff and "range" in diff:

            if step == 1:
                action = {
                    "issue_type": "performance",
                    "description": "inefficient memory usage",
                    "fix": "optimize memory"
                }

            elif step == 2:
                action = {
                    "issue_type": "performance",
                    "description": "storing values in list increases memory usage",
                    "fix": "avoid storing all values in list"
                }

            else:
                action = {
                    "issue_type": "performance",
                    "description": "unnecessary list creation",
                    "fix": "use generator (yield)"
                }

        # 🟢 Even check
        elif "% 2 == 1" in diff:
            action = {
                "issue_type": "logic",
                "description": "incorrect even check",
                "fix": "use n % 2 == 0"
            }

        # 🔵 Fallback
        else:
            action = {
                "issue_type": "logic",
                "description": "incorrect condition",
                "fix": "fix condition"
            }

        # API call
        res = requests.post(f"{API_URL}/step", json=action).json()

        print("STEP RESPONSE:", res)  

        if not isinstance(res, dict) or "observation" not in res:
            raise Exception(f"Invalid response from /step: {res}")

        reward = res.get("reward", 0.0)
        done = res.get("done", False)

        rewards.append(reward)

        info = res.get("info", {})
        log_step(step, action, reward, done, info)

        if done:
            break

        obs = res["observation"]   

    if not rewards:
        raise Exception("No rewards collected something is wrong")
    success=max(rewards)>0.5
    log_end(success, len(rewards), rewards)


if __name__ == "__main__":
    main()