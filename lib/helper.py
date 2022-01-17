# CENG 487 Assignment4 by
# Arif Burak Demiray
# December 2021

from numpy import pi


def degree_to_radian(degree: float) -> float:
    """
    This function converts a degree to its radian equivalent

    Parameters:

    Degree

    Returns:

    Radian
    """
    return degree*pi/180


def radian_to_degree(radian: float) -> float:
    """
    This function converts a radian to its degree equivalent

    Parameters:

    Radian

    Returns:

    degree
    """
    return radian*180/pi
