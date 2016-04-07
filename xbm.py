from enum import Enum

class TileContent(Enum):
    NO_ITEMS = 0
    BASIC_SHIP = 1

TileFiles ={
            TileContent.BASIC_SHIP : "@resource/images/ship.xbm"
           }
