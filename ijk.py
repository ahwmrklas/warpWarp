"""
Purpose: convert between our X and Y coordinate and a three dimensional system for finding move distances
"""

def XYtoIJK(x,y):
    i=x-int(y/2)
    j=y
    k=0 - i - j
    return i,j,k

def IJKtoXY(i,j,k):
    y = j
    x = i + int(y/2)
    return x,y
