from test.unitTest import UnitTest
from cmds import warpWarCmds

_plid = 845733184055071504452410
shipName="foobar"
foo = UnitTest(plid=_plid)
foo.loadGame("test/move_unit_test.wwr")
assert(foo.loadedGame['objects']['shipList'][0]['location']['x'] == 2 and foo.loadedGame['objects']['shipList'][0]['location']['y'] == 12)
foo.restoreGame()
assert(foo.game['objects']['shipList'][0]['location']['x'] == 2 and foo.game['objects']['shipList'][0]['location']['y'] == 12)
foo.sendCmd(warpWarCmds().moveShip(_plid, shipName, 5, 14))
foo.finishTest()
assert(foo.game['objects']['shipList'][0]['location']['x'] == 5 and foo.game['objects']['shipList'][0]['location']['y'] == 14)
