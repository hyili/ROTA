# ROTA
ROTA Game in https://www.praetorian.com/challenges/rota

## About
A ROTA game ai implemented in python3.

## Versions
- player_ai_1.py
	- The first version of game ai.
	- The policy is to apply the first found legal action.
- player_ai_2.py
	- The second version of game ai.
	- The policy is to randomly select one action from all legal actions.
- player_ai_3.py
	- The third version of game ai.
	- The policy is to use ExpectiMax Machine Learning Algorithm to learn gaming policy itself.

## Options
- ROUNDS
	- rounds of game that the ai will play, default is 10.
- ML_ENABLE
	- enable ML or not, default is True.
- LEARNING_RATE
	- learning rate of player_ai_3_py, 0 ~ 1 is allowed, default is 0.25.
