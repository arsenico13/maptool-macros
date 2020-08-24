[h: clearMacro = arg (0)]
[h: clearGroup = arg (1)]
[h: macroIndexes = getMacroIndexes (clearMacro)]
[h: macroLabels = getMacros ("json")]
[h: baseIndexes = "[]"]
[h, foreach (macroIndex, macroIndexes), code: {
	[macroProps = getMacroProps (macroIndex, "json")]
	[macroGroup = json.get (macroProps, "group")]
	[if (macroGroup == clearGroup): baseIndexes = json.append (baseIndexes, macroIndex); ""]
}]
[h: clearMacroIndexes = "[]"]
<!-- process the found macros -->
[h, foreach (macroIndex, baseIndexes), code: {
	<!-- add the base macro index to our clear list -->
	[clearMacroIndexes = json.append (clearMacroIndexes, macroIndex)]
	[macroProps = getMacroProps (macroIndex, "json")]
	[sortByBase = json.get (macroProps, "sortBy") + "-"]
	<!-- Find the macros that share the same sortBy in this macro group, remove those, also -->
	<!-- so we cant guess the label names, becuase it may be a symbol we wouldnt use right now. 
	    all we can do is list ALL macro lables, get each propertyset, and look for matches in this
	    group with the sortBy that share our base -->
	[groupMacroIndexes = dnd5e_Macro_getIndexForGroup (clearGroup)]
	[foreach (groupMacroIndex, groupMacroIndexes), code: {
		[groupMacroProps = getMacroProps (groupMacroIndex, "json")]
		[groupMacroSortBy = json.get (groupMacroProps, "sortBy")]
		[if (startsWith (groupMacroSortBy, sortByBase)): clearMacroIndexes = json.append (clearMacroIndexes, groupMacroIndex); ""]
	}]
}]
<!-- do the deed -->
<!-- eliminate duplicates -->
[h: clearMacroIndexes = json.unique (clearMacroIndexes)]
[h: log.debug (getMacroName() + ": clearMacroIndexes = " + clearMacroIndexes)]
[h, foreach (clearMacroIndex, clearMacroIndexes), code: {
	[removeMacro (clearMacroIndex)]
}]