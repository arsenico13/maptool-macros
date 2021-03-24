[h: actionObj = arg (0)]
[h: o5e_Constants (getMacroName())]
[h: saveDC = json.get (actionObj, "saveDC")]
[h, if (!isNumber (saveDC)): return (0, "")]
[h, if (saveDC <= 1): return (0, "")]
[h: saveAbility = json.get (actionObj, "saveAbility")]
[h, if (saveAbility == ""), code: {
	[log.debug (CATEGORY + "## no save ability in save object")]
	[return (0, "")]
}]
[h: saveEffect = json.get (actionObj, "saveEffect")]
[h: re = dnd5e_RollExpression_Save ("Save")]
[h: re = dnd5e_RollExpression_setSaveDC (re, saveDC)]
[h: re = dnd5e_RollExpression_setSaveAbility (re, saveAbility)]
[h: rex = dnd5e_RollExpression_setSaveEffect (re, saveEffect)]
[h: rex = dnd5e_RollExpression_setSaveEffectMultiplier (re, 0)]
[h: re = dnd5e_RollExpression_addType (re, dnd5e_Type_Targeted())]
[h: macro.return = re]