[h: re = dnd5e_RollExpression_addExpression ("{}", dnd5e_RollExpression_BuildBless())]
[h: testBlessedRe = '{"types":{"children":{"type":"children","roller":"dnd5e_DiceRoller_childRoll:75"}},"typeNames":["children"],"expressions":[{"name":"Bless","diceSize":4,"diceRolled":1,"expressionTypes":"Blessed","types":{"basic":{"type":"basic","roller":["dnd5e_DiceRoller_applyConditions:2","dnd5e_DiceRoller_basicRoll:50","dnd5e_DiceRoller_finalize:100"]}},"typeNames":["basic"]}]}']
[h: reportResults = dnd5et_Util_assertEqual (re, testBlessedRe, "Blessed Roll Expression")]
[h: macro.return = reportResults]