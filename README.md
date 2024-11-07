# 0xwizard

A digital implementation of the popular card game "Wizard" with a client-server architecture built in Python.

## 🎮 Game Overview

Wizard is a trick-taking card game where players try to predict exactly how many tricks they will win in each round. The game features:
- 60 cards (4 suits numbered 1-13, plus 4 Wizards and 4 Jesters)
- 3-6 players
- Variable number of cards per round
- Unique scoring system based on prediction accuracy

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/tadaaliia/0xwizard.git
   ```

2. Navigate to the project directory:
   ```bash
   cd 0xwizard
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the server:
   ```bash
   python server/main.py
   ```



## 🎯 Game Rules

1. **Setup**
   - First round starts with 1 card per player
   - Each subsequent round adds one card
   - Last card dealt becomes trump suit

2. **Gameplay**
   - Players predict number of tricks they'll win
   - Total predictions cannot equal number of tricks possible
   - Follow suit if possible
   - Wizard always wins
   - Jester always loses

3. **Scoring**
   - Correct prediction: 20 points + 10 points per trick
   - Incorrect prediction: -10 points per trick difference

## 🛠️ Development

### Running Tests

```bash
pytest tests/
```