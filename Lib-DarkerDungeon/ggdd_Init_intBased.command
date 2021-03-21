[h: ids = getSelected("json")]
[r, foreach(id, ids, ""), code: {
	[h: intBonus = getProperty("IntelligenceBonus", id)]
	[h, if(!isNumber(intBonus)): intBonus = 0; ""]
	[h: init = roll(1, 20) + intBonus]
	[r: "<br>" + getName(id) + " has rolled 1d20 + " + intBonus + " = " +  init + " for initiative."]
	[h: addToInitiative(0, init, id)]
}]
[h: sortInitiative()]