# Experiment findings
## Assumptions
* The board has a width of 18
* The board has a height of 17
* The board has a depth of 8 (1 + 7 layers)
* A gate cannot be linked more than 5 times
* Gates 2 is used in this experiment
* We will conduct a experiment a maximum of 10 times
  * The best results will be posted if we are unable to generate a solution
* The maximum no improve will be set at 100

## Method
* Generate a solution for a random netlist with the length of 10
* Generate a solution for a random netlist with the length of 20
* Generate a solution for a random netlist with the length of 30
* Generate a solution for a random netlist with the length of 40
* Generate a solution for a random netlist with the length of 50
* Generate a solution for a random netlist with the length of 60
* Generate a solution for a random netlist with the length of 70
* Generate a solution for a random netlist with the length of 75
* Generate a solution for a random netlist with the length of 80
* Generate a solution for a random netlist with the length of 85
* Generate a solution for a random netlist with the length of90
* Generate a solution for a random netlist with the length of 95
* Generate a solution for a random netlist with the length of 100

## Hypothesis
We are able to solve a netlist of 70 connections with our current algorithm.
However, the netlists on the Heuristics wiki are known to be solvable.
We state that our algorithm can solve _any_ netlist of 70 connections

Therefore we suspect that this experiment will prove that:

* H0 = Our algorithm can find a solution for _any_ netlist with less than 70 connections.
* H1 = Our algorithm cannot find a solution for _any_ netlist with more than 70 connections.

## Results
There is a high possiblity to have multiple gates that require to be linked 4 or 5 times, due the random nature of our new netlists
