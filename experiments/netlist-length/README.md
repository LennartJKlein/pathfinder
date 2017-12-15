# Correlation between score and length of a netlist
_Published on: 14-12-2017_

## Summary
We conducted this experiment to get a better understanding on the returned scores of the solutions. We used a set of predefined conditions (similarly to the [original case](http://heuristieken.nl/wiki/index.php?title=Chips_%26_Circuits)). In this experiment the average score of multiple lengths of netlists were compared.
This experiment showed that the score is always linearly (independent of the amount of gates, or their location, on the board) within the scope of a netlist length from 2 to 50.

See the ‘discussion’ paragraph for future improvements and extensions on this experiment.

## Background
Our program is able to solve the [6 predefined netlists](http://heuristieken.nl/resources/CC_netlists2.txt) with a length of 30 up to 70 connections.
These netlists were designed for 2 predefined boards (consisting of 25 and 50 gates).

<img src="http://heuristieken.nl/wiki/images/7/77/Print1.gif" alt="Board 1 - 25 gates" width="45%" /><img src="http://heuristieken.nl/wiki/images/1/1d/Print2.gif" alt="Board 2 - 50 gates" width="45%" />

The program we wrote for this case returns a non-deterministic solution (due to some semi-random pruning). To get a better understanding on the returned scores of the solutions, we conducted this experiment.

## Hypothesis
The score is measured by the total length of all the drawn paths on the board. The more paths, the higher the score.

H0 = We expect the score of the solution to grow linear when the length of a netlist (the amount of connections that has to be made on the board) increases.
## Method

The experiment consists of testing different lengths of netlists on different boards.
To achieve that, we did the following:
1. For each amount of gates (30, 35, 40, 45, 50 … to 95), generate a board with the gates placed randomly.
2. For each generated board, generate 50 random netlists of lengths 2, 3, 4, 5, 6 … to 50
3. _Run our program_ for every generated board:
	1. Get the average result of solving a netlist with length 2 a hundred times.
	2. Get the average result of solving a netlist with length 3 a hundred times.
	3. Get the average result of solving a netlist with length 4 a hundred times.
	4. …
	5. Plot the average *score* for every length of netlist

#### Programmatically
* Use the runXX.py files to automatically run the __main__.py in the concerned folder.
* a _runXX.py_ file will loop through the files within a map, and will loop through the maps

#### Conditions
* A board is set at a width of 18, a height of 17, a depth of 8 (1 + 7 layers).
* A gate cannot have more than 5 connections.
* The maximum ‘no improve’ of a solution is set at 5.
* Only the average score of the 50 randomly generated netlists (of the same length) will be used as results for the experiment

## Results
In the graphs below you can see the *average* scores for different lengths of netlists on different amount of gates. Every graph has a linear increase.

| | | | |
| :-: | :-: | :-: | :-: |
| **Scores at 30 gates** | **Scores at 35 gates** | **Scores at 40 gates** | **Scores at 45 gates** |
| ![30][30] | ![35][35] | ![40][40] | ![45][45] |
| **Scores at 50 gates** | **Scores at 55 gates** | **Scores at 60 gates** | |
| ![50][50] | ![55][55] | ![60][60] | |
| **Scores at 70 gates** | **Scores at 75 gates** | **Scores at 80 gates** | |
| ![70][70] | ![75][75] | ![80][80] | |

## Conclusions

Within the scope of our experiment and by the data we were able to produce, we can say that the score function increases linearly with the length of a netlist. There are two possible explanations for this phenomenon:
1. The written program always produces the best score for a netlist (which has the shortest possible paths, so the score is only depending on the amount of paths that is drawn)
2. The score function has a simple nature. If it contained more variables, it could be that the score function behaves differently.

## Discussion

After completing this experiment, we found some ways to improve and extend this experiment in the future:
1. Increase the scope of the experiment by generating netlists with a length of 50 and up. This can be used to verify or disprove the credibility of this experiment.
2. Find a way to shorten the runtime of the program (runXX.py) to generate results faster.
3. Save more data of every solution than purely the score of the board. For example:
	- if all connections were made
	- runtime of each solution
	- amount of layers needed
	- a heatmap of busy junctions on the board

[30]: https://github.com/LennartJKlein/pathfinder/blob/master/experiments/netlist-length/img/run30_score.png "scores at 30 gates"
[35]: https://github.com/LennartJKlein/pathfinder/blob/master/experiments/netlist-length/img/run35_score.png "scores at 35 gates"
[40]: https://github.com/LennartJKlein/pathfinder/blob/master/experiments/netlist-length/img/run40_score.png "scores at 40 gates"
[45]: https://github.com/LennartJKlein/pathfinder/blob/master/experiments/netlist-length/img/run45_score.png "scores at 45 gates"
[50]: https://github.com/LennartJKlein/pathfinder/blob/master/experiments/netlist-length/img/run50_score.png "scores at 50 gates"
[55]: https://github.com/LennartJKlein/pathfinder/blob/master/experiments/netlist-length/img/run55_score.png "scores at 55 gates"
[60]: https://github.com/LennartJKlein/pathfinder/blob/master/experiments/netlist-length/img/run60_score.png "scores at 60 gates"
[70]: https://github.com/LennartJKlein/pathfinder/blob/master/experiments/netlist-length/img/run70_score.png "scores at 70 gates"
[75]: https://github.com/LennartJKlein/pathfinder/blob/master/experiments/netlist-length/img/run75_score.png "scores at 75 gates"
[80]: https://github.com/LennartJKlein/pathfinder/blob/master/experiments/netlist-length/img/run80_score.png "scores at 80 gates"
[85]: https://github.com/LennartJKlein/pathfinder/blob/master/experiments/netlist-length/img/run85_score.png "scores at 85 gates"
[90]: https://github.com/LennartJKlein/pathfinder/blob/master/experiments/netlist-length/img/run90_score.png "scores at 90 gates"
[95]: https://github.com/LennartJKlein/pathfinder/blob/master/experiments/netlist-length/img/run95_score.png "scores at 95 gates"