[h: classArry = arg (0)]
[h: dnd5e_CharSheet_Constants (getMacroName())]
[h: setProperty (PROP_CLASS_OBJ, classArry)]
[h: dnd5e_CharSheet_Util_calculateProficiency ()]
[h: classStr = ""]
[h: hitDieStr = ""]
[h, foreach (classObj, classArry), code: {
	[log.debug (CATEGORY + "## classObj = " + classObj)]
	[className = json.get (classObj, "class")]
	[classLevel = json.get (classObj, "level")]
	[hitDie = json.get (classObj, "hitDie")]
	[classStr = listAppend (classStr, className + " " + classLevel, " / ")]
	[hitDieStr = listAppend (hitDieStr, classLevel + hitDie, " / ")]
}]
[h: setProperty ("Classes", classStr)]
[h: setProperty ("HitDice", hitDieStr)]