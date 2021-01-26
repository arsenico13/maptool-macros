[h: rollExpression = arg(0)]
[h: totalMultiplier = arg(1)]
[h: rolled = arg(2)]
[h: log.debug ("rollExpression: " + rollExpression)]
<!-- Check conditions -->
[h: rollExpression = dnd5e_DiceRoller_applyConditions (rollExpression)]

[h: totalRolls = json.get (rollExpression, "totalRolls")]
[h, if (totalRolls == ""): totalRolls = totalMultiplier; totalRolls = totalRolls * totalMultiplier]
[h: rolls =  "[]"]
[h: totals = "[]"]
[h: outputs = "[]"]
[h: allTotal = 0]

[h: children = dnd5e_RollExpression_getExpressions (rollExpression)]
[h, if (!json.isEmpty (children)), code: {
	<!-- We have to roll the children in multiples of the parents totalRolls -->
	[children = dnd5e_DiceRoller_roll (children, totalRolls)]
	[rollExpression = dnd5e_RollExpression_setExpressions (rollExpression, children)]
}; {""}]

[h, for (i, 0, totalRolls), code: {
	<!-- clear the output, we capture multiple outputs in an array -->
	[h: rollExpression = json.set (rollExpression, "output", "")]

	<!-- Build a stack (array) of rollers -->
	<!-- The array has been ordered based on roller priority (defined by the Types) -->
	[rollers = dnd5e_RollExpression_getDiceRollers (rollExpression)]
	[log.debug (getMacroName() + ": rollers = " + rollers)]
	[rollExpression = json.set (rollExpression, "rollers", rollers, "remainingRollers", rollers)]
	[while (!json.isEmpty(rollers)), code: {
		[roller = json.get (rollers, 0)]
		[rollers = json.remove (rollers, 0)]
		[log.debug (getMacroName() + ": remaining rollers = " + rollers)]
		[rollExpression = json.set (rollExpression, "remainingRollers", rollers)]
		<!-- For each roller, send RE to roller and capture return RE. Return RE has been fully
			processed and is considered "roll". Re-roll rules have already been applied by
			the related roller(s) -->
		[log.debug (getMacroName() + ": rolling " + roller)]
		[evalMacro ( "[rollExpression = " + roller + "(rollExpression)]")]

		<!-- Some rollers interrupt the rolling stack, so we have to re-fetch the remaining
				rollers stack. Typically, these rollers zero out the stack, but some may decide
				to push something new on the stack -->
		[rollers = json.get (rollExpression, "remainingRollers")]
	}]
	[h: rollExpression = dnd5e_DiceRoller_finalize (rollExpression)]
	[h: rollExpression = dnd5e_RollExpression_buildOutput (rollExpression)]
	[h: output = dnd5e_RollExpression_getOutput (rollExpression)]
	[h: outputs = json.append (outputs, output)]
}]

[h: rollExpression = json.set (rollExpression, "outputs", outputs)]
[h: totals = json.get (rollExpression, "totals")]
[h: allTotal = 0]
[h, foreach (totalVal, totals): allTotal = allTotal + totalVal]
[h: rollExpression = json.set (rollExpression, "allTotal", allTotal)]
[h: macro.return = rollExpression]