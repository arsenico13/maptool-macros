[h: doAbort = arg(0)]
[h: l4m.Constants()]
[h: callStack = getLibProperty (CALL_STACK, LIB_LOG4MT)]
[h: doStack = 1]
[h: lastCall = ""]
[h: stackSize = json.length (callStack)]
[h, if (stackSize > 0): lastCall = json.get (callStack, json.length (callStack) - 1)]
[h, if (lastCall == MACRO_ABORT || stackSize == 0): doStack = 0]
[h, if (!doAbort && doStack), code: {
	[callStack = getLibProperty (CALL_STACK, LIB_LOG4MT)]
	[callStack = json.append (callStack, MACRO_ABORT)]
	[setLibProperty (CALL_STACK, callStack, LIB_LOG4MT)]
}]
[h: oldFunction (doAbort)]