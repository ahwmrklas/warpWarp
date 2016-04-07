from enum import Enum

#The enum with all the types of things we want to be able to put in a tile.
#Right now, everything in here should also have an entry in the TileFiles dict.
class TileContent(Enum):
    NO_ITEMS = 0
    BASIC_SHIP = 1

#Every value in this dict should be a xbm file in the resource/images dir.
#The "@" prefix is required by create_polygon.
TileFiles = {
        TileContent.NO_ITEMS : '', #no items, no xbm file
        TileContent.BASIC_SHIP : "@resource/images/ship.xbm"
        }
