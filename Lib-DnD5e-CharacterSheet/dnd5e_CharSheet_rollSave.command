[h: saveName = arg (0)]
[h: dnd5e_CharSheet_Constants (getMacroName())]
[h: log.debug (CATEGORY + "## saveName = " + saveName)]
[h: re = dnd5e_RollExpression_Save (saveName)]
[h: re = dnd5e_RollExpression_addPropertyModifiers (re, saveName + "Save")]
[h: log.debug (CATEGORY + "## re = " + re)]
[h: rolled = dnd5e_DiceRoller_roll (re)]
[h: log.debug (CATEGORY + "## rolled = " + rolled)]
[r: token.name + ": "]
[r: dnd5e_RollExpression_getOutput (json.get (rolled, 0))]