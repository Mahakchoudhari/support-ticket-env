from pydantic import BaseModel

# Models
class Observation(BaseModel):
    ticket: str
    last_action: str
    feedback: str


# Tasks
TASKS = [
    {
        "id": "easy",
        "ticket": "I was charged twice for my order",
        "label": "billing",
        "action": "refund"
    },
    {
        "id": "medium",
        "ticket": "My internet is not working since morning",
        "label": "technical",
        "action": "troubleshoot"
    },
    {
        "id": "hard",
        "ticket": "I want a refund, product is damaged and support not responding",
        "label": "refund",
        "action": "refund"
    }
]


# Grader
def grade_classification(pred, actual):
    return 1.0 if pred.lower() == actual else 0.0


def grade_action(pred, actual):
    if pred.lower() == actual:
        return 1.0
    elif pred.lower() in ["refund", "escalate", "troubleshoot"]:
        return 0.5
    return 0.0


def grade_response(response):
    keywords = ["sorry", "help", "resolve", "refund"]
    score = sum(1 for k in keywords if k in response.lower())
    return min(score / len(keywords), 1.0)


def final_score(cls, act, resp):
    return 0.3 * cls + 0.3 * act + 0.4 * resp


# Environment
class SupportEnv:

    def __init__(self):
        self.current_task = None
        self.step_count = 0

    def reset(self, task_id=0):
        self.current_task = TASKS[task_id]
        self.step_count = 0
        self.history = {}

        return self._get_obs("Environment reset")

    def step(self, action):
        self.step_count += 1

        reward = 0.0
        done = False
        feedback = ""

        if action["type"] == "classify":
            score = grade_classification(action["content"], self.current_task["label"])
            self.history["classification"] = score
            reward = score
            feedback = f"classification score: {score}"

        elif action["type"] == "act":
            score = grade_action(action["content"], self.current_task["action"])
            self.history["action"] = score
            reward = score
            feedback = f"action score: {score}"

        elif action["type"] == "respond":
            score = grade_response(action["content"])
            self.history["response"] = score

            final = final_score(
                self.history.get("classification", 0),
                self.history.get("action", 0),
                score
            )

            reward = final
            done = True
            feedback = f"final score: {final}"

        return self._get_obs(feedback), reward, done, {}

    def state(self):
        return {
            "task": self.current_task,
            "history": self.history,
            "steps": self.step_count
        }

    def _get_obs(self, feedback):
        return {
            "ticket": self.current_task["ticket"],
            "last_action": "",
            "feedback": feedback
        }