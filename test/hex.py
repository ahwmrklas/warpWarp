'''
Trying to draw regular hexagons in a window with Tkinter.
'''

# Reference: http://infohost.nmt.edu/tcc/help/pubs/tkinter/create_polygon.html

# Notes:
# To erase: delete(id) or delete(ALL)
# To work on the individual widgets (hexagons): itemconfig, coords

from Tkinter import *
from math import cos, sin, pi

def poly(n, xscale=None, yscale=None, posx=None, posy=None,
         linewidth=1, fill='', tags=''):
    
    '''
    Draws an n-gon with color set by fill, tagged with tags
    (space separated). Returns the objectID.
    '''
    if xscale is None: xscale = float(canvas['width'])/2
    if yscale is None: yscale = float(canvas['height'])/2
    if posx is None: posx = float(canvas['width'])/2 + .5
    if posy is None: posy = float(canvas['height'])/2 + .5
    
    xscale, yscale = float(xscale), float(yscale)
    posx, posy = float(posx), float(posy)
    polypoints = []
    for i in range(n + 1):
        theta = i * pi*2/n
        x = posx + xscale * cos(theta)
        y = posy - yscale * sin(theta)
        polypoints.append(x)
        polypoints.append(y)
    
    return canvas.create_polygon(fill=fill, outline='black',
                                 width=linewidth, tags=tags, *polypoints)


def draw(w=None, h=None):
    cols = {
        10:'red', 9:'green', 8:'blue', 7:'yellow', 6:'purple',
         5:'red', 4:'green', 3:'blue', 2:'yellow', 1:'purple'
    }
    if w is None: w = float(canvas['width'])
    if h is None: h = float(canvas['height'])
    
    for size in range(10, 0, -1):
        xscale, yscale = (size/10.0 * w/2), (size/10.0 * h/2)
        id = poly(6,
                  xscale=xscale, yscale=yscale,
                  posx=w/2, posy=h/2,
                  linewidth=size/2, fill=cols[size])

def click(event):
    print( 'click!', canvas.winfo_containing(event.x, event.y))

def resize(event):
    canvas.delete(ALL)
    draw(event.width, event.height)


def run():
    canvas.bind('<Button-1>', click)
    canvas.bind('<Configure>', resize)
    draw()
    frame.mainloop()

if __name__=='__main__':
    frame = Frame(width=500, height=200, bg='blue')
    canvas = Canvas(frame, bg='white')
    canvas.pack(fill=BOTH, expand=YES)
    frame.pack(fill=BOTH, expand=YES)
    run()
