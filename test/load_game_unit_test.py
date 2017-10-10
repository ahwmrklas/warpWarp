from test.unitTest import UnitTest
from cmds import warpWarCmds
from dataModel import emptyGame

_plid = 845733184055071504452410
shipName="foobar"
foo = UnitTest(plid=_plid)
foo.loadGame("test/move_unit_test.wwr")
assert(foo.loadedGame != emptyGame())
foo.restoreGame()
assert(foo.loadedGame == foo.game)
foo.finishTest()
