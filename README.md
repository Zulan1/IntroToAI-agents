# Project Information

This project is using Python 3.11.

## Installation

1. (Optional) Create a venv using: "python3 -m venv venv".
2. (Optional) Activate venv using: "./venv/Scripts/activate"(Windows) or "source ./venv/bin/activate/" on linux
3. (On Linux) Make sure TkAgg backend (already defined in ./agents/human_agent.py) is used and Tkinter is installed on the machine.
4. Install python packages using: "pip install -r requirements.txt"
5. Configure config.ini with grid configuration file, A* limit, and RTA* L.
6. You can use the available tests ./tests/.
7. Run the code with "python .".

## Clarification

The Agents available for this projects are:

1. Human Agent (denoted as H in the test file) should always be in the test for debugging.
2. Interfering Agent (denoted as I in the test file) can always be in the test but not a must.
3. Stupid Greedy Agent (denoted as SG in the test file) a simple agent that solves the problem using Dijkstra's Algorithm.
4. Greedy Agent (denoted as G in the test file) an agent solving the problem using a heuristic function to evaluate the next move.
5. A* Agent (denoted as A in the test file) an agent solving the problem using the regular A* algorithm with a few improvements.
6. RTA* Agent (denoted as RTA in the test file) an agent solving the problem using the same A* algorithm but gives up after a number of expansions and gives the best move that was found.
7. Multi Agent (denoted as MA in the test file) an agent solving the problem give 2 A* agents. Tests 8-11 in the solvable section are example for that.
8. Multi Agent 2 (denoted as MA2 in the test file) same as in section 7 but with a different, simpler heuristic.









