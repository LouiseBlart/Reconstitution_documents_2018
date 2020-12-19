#!/usr/bin/python3
# -*- coding: utf-8 -*-

import random


#:a constant for the black color
black = (0,0,0)

#:a constant for the white color
white = (255,255,255)

#:a constant for the red color
red = (255,0,0)

#:a constant for the blue color
blue = (0,0,255)

#:a constant for the green color
green = (0,255,0)


def brightness(c):
    """
    Return the brigthness of a color

    :param c: a color
    :type c: (int,int,int)
    :rtype: a float between 0.0 and 1.0
    :return: the brightness of the color c
    """
    r,g,b = c
    return (r+g+b) / (3*255)

