# Pathfinder

A program that uses wires to connect gates on a chip three-dimensionally and efficiently. Based on the case of [Chips & Circuits](http://heuristieken.nl/wiki/index.php?title=Chips_%26_Circuits).

Chips (or more precisely: integrated circuits) are found in your PC, MacBook, Android Phone and microwave oven where they perform a diversity of functions, ranging from timekeeping and motor control to arithmetic and logic. Basically a small plate of silicon, chips are usually designed logically and subsequentially transformed to a list of connectable gates. This list, commonly known as a net list is finally transformed into a 2-dimensional design on a silicon base.

This last step however, the physical real-world process of connecting the gates, is highly volatile. Good arrangements on the base lead to short connections, leading to faster circuits, whereas poor arrangements lead to slower circuits. It leads to no doubt that a good arrangement of logical gates and good wiring between them is of vital essence to the performance of the IC as a whole (source: http://heuristieken.nl/wiki/index.php?title=Chips_%26_Circuits).

The algorithms and content of the sample is ben setup to create paths from predefined net lists and two boards that can be found in sample/data. So in short, the aim is to connect the dots (gates) in a efficient manner.

# Notable content:

## Docs/html
The [documentations](https://lennartjklein.github.io/pathfinder/) of the classes and helper functions used in sample. The documentations are made by Sphinx, a docstring converter.

## Experimtents
One experiment is documented at the moment. We used a random netlist creator and random board creator to see how the used algorithms preformed.

## Sample
Sample is the core of our repository! \__main.\__.py is the core of the core. It makes use of classes.py and helpers.py to drive the algorithems to solve the case.
Aditions are colors.py for adding terminal colors and settings.py. settings.py can be used to modify the program but more on that in de README.md in the sample directory.


# Requirements

To run this program, you need the following:

* Python 3.6.3
* [numpy](http://www.numpy.org/) 1.13.3
* [matplotlib](https://matplotlib.org/index.html) 2.1.0

# Installation

Clone or download this repository (containing the pathfinder module) to a folder of your preference. And make sure the requirements above are installed.

# Contributing

This project is not open for contributing at the moment,2 for it being a school assignment.

# Versioning

We use [SemVer](http://semver.org/) for semantic versioning. For the versions available, see the [tags on this repository](https://github.com/LennartJKlein/chips-circuits/tags).

# Authors

* **Jurre Brandsen** - *Developer* - [www.jurrebrandsen.nl](http://www.jurrebrandsen.nl/)
* **Lennart Klein** - *Webdeveloper and webdesigner* - [www.lennartklein.nl](http://www.lennartklein.nl/)
* **Thomas de Lange** - *Developer* - [www.long-coding.nl](http://www.long-coding.nl/)

# License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

# Acknowledgments

* Thanks to Daan van den Berg for creating the "Chips and circuits" case (as specified on [this Wiki](http://heuristieken.nl/wiki/index.php?title=Chips_%26_Circuits)).
* Thanks to Westly White for his [initial grid design](https://stackoverflow.com/questions/41619600/numbering-rows-and-columns-in-a-grid-board) in board.py.
