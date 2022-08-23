PYTHON = python3

# This target is executed whenever we just type `make`
.DEFAULT_GOAL = help

# The @ makes sure that the command itself isn't echoed in the terminal
help:
	@echo "---------------HELP-----------------"
	@echo "For Q-1 type make q1"
	@echo "For Q-2 type make q2"
	@echo "For Q-3 type make q3"
	@echo "------------------------------------"	
	
ques1:
	@echo "ipynb converted to .py for namesake"
	@${PYTHON} q1.py

ques2:
	@echo "ipynb converted to .py for namesake"
	@${PYTHON} q2.py

ques3:
	@echo "ipynb converted to .py for namesake"
	@${PYTHON} q3.py
