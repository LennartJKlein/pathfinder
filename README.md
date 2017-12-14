# Pathfinder

A program that uses wires to connect gates on a chip three-dimensionally and efficiently. Based on the case of [Chips & Circuits](http://heuristieken.nl/wiki/index.php?title=Chips_%26_Circuits)

## Requirements

To run this program, you need the following:

* Python 3.6

## Installation

Clone this repository (containing the pathfinder module) to a folder of your preference. And run the setup:

```
python setup.py install
```

## Documentation
Learn how to install, test, use and integrate this program that finds efficient paths in the [documentation](docs/index.md).

## Definitions:
*Board*: The board a three dimensional grid with a presetted height, weight and depth.

*Gate*: A gate is placed on the surface of the board and can be connected to another gate.

*Connection*: Two gates that have to be linked, whereas gate A is the starting point and gate B is the end point.

*Path*: A path from gate to gate, walking over the board. It cannot move diagonally only in one of six directions: north, south, west, east, up and down. 

*Netlist*: A list of connections

*Score* of a board: The total sum of the lengths of all connected paths.

*Result* of a board: The percentage of made connections from the netlist.

*Solvability of a board*: The average calculated percentage of a board with randomly placed gates and random netlists.


## Contributing

This project is not open for contributing, for it being a school assignment.

## Versioning

We use [SemVer](http://semver.org/) for semantic versioning. For the versions available, see the [tags on this repository](https://github.com/LennartJKlein/chips-circuits/tags).

## Authors

* **Jurre Brandsen** - *Developer* - [www.jurrebrandsen.nl](http://www.jurrebrandsen.nl/)
* **Lennart Klein** - *Webdeveloper and webdesigner* - [www.lennartklein.nl](http://www.lennartklein.nl/)
* **Thomas de Lange** - *Initial work* - [www.long-coding.nl](http://www.long-coding.nl/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* Thanks to Daan van den Berg for creating the "Chips and circuits" case (as specified on [this Wiki](http://heuristieken.nl/wiki/index.php?title=Chips_%26_Circuits)).
* Thanks to Westly White for his [initial grid design](https://stackoverflow.com/questions/41619600/numbering-rows-and-columns-in-a-grid-board) in board.py.
