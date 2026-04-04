# 🧠 Support Ticket OpenEnv Environment

## 🚀 Overview

This project implements a real-world OpenEnv environment simulating a **customer support ticket resolution system**.
An AI agent interacts with the environment to analyze and resolve user complaints through structured decision-making steps.

---

## 💡 Motivation

Customer support automation is widely used in real-world systems such as:

* Helpdesk platforms
* Chatbots
* Email support systems

This environment models a realistic workflow where an agent must:

1. Understand the problem
2. Take appropriate action
3. Provide a meaningful response

---

## 🎯 Tasks

The environment includes **3 tasks with increasing difficulty**:

### 🟢 Easy — Ticket Classification

* Classify ticket into:

  * billing
  * technical
  * refund

---

### 🟡 Medium — Action Selection

* Choose correct action:

  * refund
  * troubleshoot
  * escalate

---

### 🔴 Hard — Full Resolution

* Perform full pipeline:

  * classification
  * action selection
  * response generation

---

## 🧠 Action Space

```json
{
  "type": "classify | act | respond",
  "content": "string"
}
```

---

## 👀 Observation Space

```json
{
  "ticket": "string",
  "last_action": "string",
  "feedback": "string"
}
```

---

## 🎯 Reward Function

The reward function provides continuous feedback:

* Classification score → 0.0 to 1.0
* Action score → 0.0 to 1.0
* Response quality → keyword-based scoring

### Final Score

```
Final Score = 0.3 * classification + 0.3 * action + 0.4 * response
```

### Additional Features

* Penalizes inefficient behavior (extra steps)
* Encourages correct multi-step reasoning

---

## ⚙️ Environment API

The environment follows OpenEnv standards:

* `reset()` → Initializes environment
* `step(action)` → Returns (observation, reward, done, info)
* `state()` → Returns current internal state

---

## 🧪 Baseline Agent

A deterministic rule-based agent is provided:

* No external API required
* Fully reproducible results
* Stable evaluation

---

## 📊 Baseline Scores

| Task   | Score |
| ------ | ----- |
| Easy   | ~1.0  |
| Medium | ~0.7  |
| Hard   | ~0.8  |

---

## ▶️ How to Run the Project

### 🖥️ 1. Open Terminal / Command Prompt

Navigate to the project folder:

```bash
cd OneDrive\Desktop\support-ticket-env
```

---

### 📦 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### ▶️ 3. Run the Environment

```bash
python inference.py
```

---

### ✅ Expected Output

```text
[START]
[STEP] action: {'type': 'classify', 'content': 'billing'}
[STEP] reward: 1.0
[STEP] action: {'type': 'act', 'content': 'refund'}
[STEP] reward: 1.0
[STEP] action: {'type': 'respond', 'content': '...'}
[STEP] reward: 0.8
[END] total_score: 2.x
```

---

## 🐳 Docker Setup (Optional)

### Build image

```bash
docker build -t support-env .
```

### Run container

```bash
docker run support-env
```

---

## 📁 Project Structure

```
support-ticket-env/
│
├── support_env.py
├── inference.py
├── openenv.yaml
├── Dockerfile
├── requirements.txt
├── README.md
```

---

## ✅ Key Features

* Real-world task simulation
* Multi-step reasoning
* Deterministic grading system
* Continuous reward feedback
* Safe execution (no infinite loops)
* Lightweight and reproducible

---

## 🚀 Future Improvements

* LLM-based response grading
* Multi-turn conversations
* Sentiment-aware responses
* Larger ticket dataset

---

## 🏆 Conclusion

This project provides a realistic and structured benchmark for evaluating AI agents in customer support workflows.
It ensures reproducibility, clarity, and real-world relevance.

---
