# Data

This map contains the data we used to solve the Chips & Circuits case.

## Detailed explanation

*gatesXX.csv:*

All gate files have the following set-up:
	   col 1:  col2:  col3:  col4:
row 1: name    x      y      z
row 2: 1	   nr     nr     nr
row 3: 2       nr     nr     nr
_etc_

* gates0.csv: This is a very small test file. This was used in the early development of our program
* gates1.csv: This is the small composition of 25 gates
* gates2.csv: This is the large composition of 50 gates

*netlistXX.txt*

All netlist files have the following set-up:
row1: [(touple a, touple b), (touple a, touple b), (touple a, touple b), (touple a, touple b), _etc_]

* netlist0.txt: This is a very small test file. This was used in the early development of our program
* netlist1: list of 30 connections. This is used for gates1.csv
* netlist2: list of 40 connections. This is used for gates1.csv
* netlist3: list of 50 connections. This is used for gates1.csv
* netlist4: list of 50 connections. This is used for gates2.csv
* netlist5: list of 60 connections. This is used for gates2.csv
* netlist6: list of 70 connections. This is used for gates2.csv