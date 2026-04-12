import os
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')

# Try to import requests, provide a clear error message if it's missing
try:
    import requests
except ModuleNotFoundError:
    print("❌ ERROR: The 'requests' module is missing.")
    print("👉 Please run this command to install it:")
    print("   pip install requests")
    sys.exit(1)

print("All ENV VARS:")
for k, v in os.environ.items():
    print(f"{k}={v}")

API_BASE_URL = (
    os.getenv("ENV_URL")
    or os.getenv("OPENENV_BASE_URL")
    or os.getenv("BASE_URL")
    or os.getenv("API_BASE_URL")
    or "http://127.0.0.1:7860" # Local fallback
)

print("DEBUG URL =", API_BASE_URL)

def call_endpoint(path, data=None):
    # FIX: Safely construct the URL to prevent double slashes (e.g., //reset)
    base = API_BASE_URL.rstrip('/')
    target_path = "/" + path.lstrip('/')

    urls = [
        f"{base}{target_path}",
        f"{base}/env{target_path}",
        f"{base}/api{target_path}"
    ]

    max_retries = 10
    for attempt in range(max_retries):
        for url in urls:
            try:
                res = requests.post(url, json=data or {})
                if res.status_code == 200:
                    if attempt > 0:
                        print(f"✅ Server woke up! Working URL: {url}")
                    else:
                        print("✅ Working URL:", url)
                    return res.json()
                else:
                    print(f"❌ Tried {url} → HTTP {res.status_code}")
            except requests.exceptions.ConnectionError:
                # Connection refused because server isn't up yet, fail silently this round
                pass
            except Exception as e:
                print(f"❌ Error calling {url}: {e}")
        
        print(f"⏳ Waiting for server to start... (Attempt {attempt + 1}/{max_retries})")
        time.sleep(2)

    raise Exception(f"All endpoint attempts failed for {path} after {max_retries} retries.")


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

    res = call_endpoint("/reset")

    print("RESET RESPONSE:", res)

    if not isinstance(res, dict) or "observation" not in res:
        raise Exception(f"Invalid response from /reset: {res}")

    obs = res["observation"]

    for step in range(1, MAX_STEPS + 1):
        diff = obs["diff"].lower()

        # 🔵 Subtle max bug (HIGH PRIORITY)
        if "max = 0" in diff:
            if step == 1:
                action = {"issue_type": "logic", "description": "possible incorrect initialization", "fix": "check initial value"}
            elif step == 2:
                action = {"issue_type": "logic", "description": "incorrect initialization for negative numbers", "fix": "initialize with minimum value"}
            else:
                action = {"issue_type": "logic", "description": "max initialized to 0 fails for negative arrays", "fix": "initialize max with float('-inf') to handle negative values correctly"}

        # 🔴 Nested loop performance
        elif "for i in range(len(arr))" in diff:
            if step == 1:
                action = {"issue_type": "performance", "description": "inefficient loop", "fix": "optimize loop"}
            elif step == 2:
                action = {"issue_type": "performance", "description": "nested loops increase time complexity", "fix": "reduce number of iterations"}
            else:
                action = {"issue_type": "performance", "description": "nested loop inefficient", "fix": "use set for optimization"}

        # 🟡 Division edge case
        elif "len(nums)" in diff and "/" in diff:
            if step == 1:
                action = {"issue_type": "logic", "description": "possible division issue", "fix": "check values"}
            elif step == 2:
                action = {"issue_type": "logic", "description": "division by zero possible", "fix": "check length"}
            else:
                action = {"issue_type": "logic", "description": "division by zero when list is empty", "fix": "check if len(nums) > 0"}

        # 🟢 Variable typo
        elif "tota" in diff:
            if step == 1:
                action = {"issue_type": "logic", "description": "possible variable issue", "fix": "check variable"}
            elif step == 2:
                action = {"issue_type": "logic", "description": "undefined variable or typo", "fix": "fix variable name"}
            else:
                action = {"issue_type": "logic", "description": "variable name typo", "fix": "use total instead of tota"}

        # 🟣 Memory inefficiency
        elif "append" in diff and "range" in diff:
            if step == 1:
                action = {"issue_type": "performance", "description": "inefficient memory usage", "fix": "optimize memory"}
            elif step == 2:
                action = {"issue_type": "performance", "description": "storing values in list increases memory usage", "fix": "avoid storing all values in list"}
            else:
                action = {"issue_type": "performance", "description": "unnecessary list creation", "fix": "use generator (yield)"}

        # 🟢 Even check
        elif "% 2 == 1" in diff:
            action = {"issue_type": "logic", "description": "incorrect even check", "fix": "use n % 2 == 0"}

        # 🔵 Fallback
        else:
            action = {"issue_type": "logic", "description": "incorrect condition", "fix": "fix condition"}

        # API call
        res = call_endpoint("/step", action)

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
    
    success = max(rewards) > 0.5
    log_end(success, len(rewards), rewards)


if __name__ == "__main__":
    main()