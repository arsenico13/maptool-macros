[h: macros = getMacros()]
[h: log.debug ("macros: " + macros)]
[h, foreach (macroName, macros), code: {
	[h, if (lastIndexOf (macroName, "jse.") > -1), code: {
		[h: log.debug ("Registering " + macroName)]
		[h: defineFunction (macroName, macroName + "@this")]
	}]
}]