[h: id = arg(0)]
[h: condExp = arg(1)]
[h: state = arg(2)]
[h, if (json.length(macro.args) > 3): saveExp = arg(3); saveExp = "{}"]
[h: log.debug(getMacroName() + ": args=" + json.indent(macro.args))]

<!-- No save needed? -->
[h, if (json.isEmpty(saveExp)), code: {
	[h: tt = "Setting State"]
	[h: addStates = 1]
}; {

	<!-- Handle the save -->
	[h: save = if(json.get(saveExp, "saveResult") == "passed", 1, 0)]
	[h: need = if(json.get(condExp, "saveResult") == "pass", 1, 0)]
	[h: tt = "DC " + dnd5e_RollExpression_getSaveDC(saveExp) + " " + dnd5e_RollExpression_getSaveAbility(saveExp) + ": "]
	[h: tt = tt + dnd5e_RollExpression_getTypedDescriptor(saveExp, "tooltipRoll") + " = " 
			+ dnd5e_RollExpression_getTypedDescriptor(saveExp, "tooltipDetail") + " = " + dnd5e_RollExpression_getTotal(saveExp)]
	[h: tt = tt + ": Save has " + if(save, "Passed", "Failed") +  ", need save to " + if(need, "Pass", "Fail")]
	[h: addStates = if(save == need, 1, 0)]
	[h: tt = tt + ": " + if(addStates, "Setting", "Ignoring") + " State"]
}]
[h: log.debug(getMacroName() + ": addStates=" + addStates + " tt=" + tt + " conditions=" + json.indent(json.get(condExp, "conditions")))]
[h: input("bob|1|" + getMacroName() + "|TEXT")]

<!-- Apply the states -->
[h: output = json.get(state, "output") + "<i>"]
[h, foreach(cond, json.get(condExp, "conditions")), code: {
	[h, if (addStates): setState(cond, 1, id)]
	[h: output = output + " " + if(!addStates, "<s>", "") + "<span title='" + tt + "'>" + cond + "</span>" + if(!addStates, "</s>", "") + ","]
}]
[h: output = output + "</i>"] 
[h: state = json.set(state, "output", output)]
[h: macro.return = state]