<pre>

Get a copy of the repository:

    git clone git@192.168.0.4:repos/warpWar

You need "git" and a key.

Generate a key like this.
    ssh-keygen -C "your email address"
Then email dad the resulting file "id_rsa.pub"
Dad will append that file to the authorized keys on the "git" account.
cat name.id_rsa.pub >> ~git/.ssh/authorized_keys

You need to install python3 and git.
smartgit works for windows but you still need the ssh keys. Possibly generate
them on linux and install the private key on windows.
=======

Start the server and the client and the map
python3 STest.py &
python3 CTest.py &
python3 main.py &

=======

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

-----
Note to future versions of Alex. Dad won the star/starbase resource argument. stop having it.
