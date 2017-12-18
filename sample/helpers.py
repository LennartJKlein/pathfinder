"""Helper functions used in __main__.py.

Name: helpers.py

Authors:
    - Jurre Brandsen
    - Lennart Klein
    - Thomas de Lange

LICENSE: MIT
"""


def calculate_distance(a, b):
    """Calculate the distance between two points on the board (manhatan).

    :type a: tuple
    :param a: the first point on the board

    :type b: tuple
    :param b: the second point on the board

    :rtype: interger
    """
    dx = (a[2] - b[2]) ** 2
    dy = (a[1] - b[1]) ** 2
    dz = (a[0] - b[0]) ** 2
    return (dx + dy + dz) ** 0.5


def calculate_delta(a, b):
    """Delta distance between two coords.

    :type a: tuple
    :param a: starting coord

    :type b: tuple
    :param b: goal coord

    :rtype: interger
    """
    dx = abs(a[2] - b[2])
    dy = abs(a[1] - b[1])
    dz = abs(a[0] - b[0])
    return dx + dy + dz
