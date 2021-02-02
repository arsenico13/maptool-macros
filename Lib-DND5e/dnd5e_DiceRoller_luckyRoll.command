[h: rollExpression = arg (0)]
[h: log.debug (getMacroName() + ": rolling " + rollExpression)]
[h: luckyRolls = json.get (rollExpression, "luckyRolls")]
[h: roll = json.get (rollExpression, "roll")]
[h, if (roll == 1 && luckyRolls > 0), code: {
	[h: log.debug ("dnd5e_DiceRoller_luckyRoll: Rerolling 1")]
	[h: luckyRolls = luckyRolls - 1]
	[h: rollExpression = json.set (rollExpression, "luckyRolls", luckyRolls)]
	[h: maxPriority = dnd5e_Type_getPriority (dnd5e_Type_Lucky(), getMacroName())]
	[h: rolled = dnd5e_DiceRoller_roll (rollExpression)]
	[h: rollExpression = json.get (rolled, 0)]
	[h: description = "<b>Lucky!</b> 1 rerolled: " + 
		json.get (rollExpression, "roll") + "<br>New total: " + json.get (rollExpression, "total")]
	[h: rollExpression = dnd5e_RollExpression_addDescription (rollExpression, description)]
	[h: rollExpression = dnd5e_RollExpression_addTypedDescriptor(rollExpression, "lucky", "(lucky reroll)", 0)]
}]
[h: macro.return = rollExpression]
