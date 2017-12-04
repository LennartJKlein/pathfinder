def calculate_distance(a, b):
    """
    Args:
        a(touple): Starting coord
        b(touple): Goal coord

    Return:
        Distance between two coords
    """

    dx = (a[2] - b[2]) ** 2
    dy = (a[1] - b[1]) ** 2
    dz = (a[0] - b[0]) ** 2
    return (dx + dy + dz) ** 0.5

def calculate_delta(a, b):
    """
    Args:
        a(touple): Starting coord
        b(touple): Goal coord

    Return:
        Delta distance between two coords
    """

    dx = abs(a[2] - b[2])
    dy = abs(a[1] - b[1])
    dz = abs(a[0] - b[0])
    return dx + dy + dz