[h: actionName = arg (0)]
[h: actionObj = arg (1)]
[h, if (json.length (macro.args) > 2): advDisadv = arg (2); advDisadv = "none"]

[h: attackType = json.get (actionObj, "attackType")]
[h, if (attackType == "Melee"): ability = "Strength"; ability = "Dexterity"]
[h: abilityBonus = eval (ability + "Bonus")]
[h: attackBonus = json.get (actionObj, "attackBonus") + abilityBonus]
[h: attackExpression = dnd5e_RollExpression_Attack (actionName, attackBonus)]
[h: attackExpression = dnd5e_RollExpression_setAdvantageDisadvantage (attackExpression, advDisadv)]

[h: damageExpression = o5e_RollExpression_forDamageFromAttackAction (actionObj, abilityBonus)]
[h, if (encode (damageExpression) != ""): rollExpressions = json.append ("", attackExpression, damageExpression); ""]
[h: extraObjs = json.get (actionObj, "extraDamage")]
[h, foreach (extraObj, extraObjs), code: {
	[extDamageExpression = o5e_RollExpression_forDamageAction (extraObj)]
	[if (encode (extDamageExpression) != ""): rollExpressions = json.append (rollExpressions, extDamageExpression); ""]
}]

[h: macro.return = rollExpressions]