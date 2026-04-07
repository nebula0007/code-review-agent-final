from app.models import Observation, Action, StepResult, Task
from app.tasks import TASKS
from app.grader import grade_action
import random


class CodeReviewEnv:

    def __init__(self):
        self.current_task: Task | None = None
        self.done: bool = False
        self.steps: int = 0
        self.max_steps: int = 3

    # 🔁 Reset environment
    def reset(self) -> Observation:
        self.current_task = random.choice(TASKS)
        self.done = False
        self.steps = 0  # reset step counter

        return Observation(
            diff=self.current_task.diff,
            task_type=self.current_task.issue_type
        )

    # ▶️ Step
    def step(self, action: Action) -> StepResult:
        if self.done:
            raise Exception("Episode already finished. Call reset().")

        # Calculate reward
        reward = grade_action(action, self.current_task)

        # Increment step count
        self.steps += 1

        # Done logic
        if reward == 1.0:
            self.done = True
        elif self.steps >= self.max_steps:
            self.done = True
        else:
            self.done = False

        # Observation stays same (same task)
        observation = Observation(
            diff=self.current_task.diff,
            task_type=self.current_task.issue_type
        )

        return StepResult(
            observation=observation,
            reward=reward,
            done=self.done,
            info={
                    "task_id": self.current_task.id,
                    "step": self.steps,
                    "debug_done": self.done,
                    "debug_reward": reward
                 }
        )

    # 📊 State (for debugging / API)
    def state(self):
        return {
            "task_id": self.current_task.id if self.current_task else None,
            "done": self.done,
            "steps": self.steps
        }