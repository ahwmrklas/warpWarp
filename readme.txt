<pre>

Get a copy of the repository:

    git clone git@192.168.0.4:repos/warpWar

You need "git" and a key.

Generate a key like this.
    ssh-keygen -C "<your email address"
Then email dad the resulting file "id_rsa.pub"
=========

rules: http://www.contrib.andrew.cmu.edu/usr/gc00/reviews/warpwar.html
Map
hexes
planets
warp lines

Players
decision makers
    human
    computer
network connection

Options:
What to purchase
How to use purchased items
Where to place new units
Where to move: Direction, how far
Where to attack
Which attack action and how powerful
Retreat option

Ships

Combat

Resources for building

victory conditions
-------------
Print the grid/map


------
data model proposal:

class Game():
    playerList
    supplies
    activePlayer
    sockets
    map
    turnNum
    techLevel

class Player():
    shipList
    baseList
    buildPoints

class Ship():
    techLevel
    shipStats
    supplies
    location

class Base()
</pre>
