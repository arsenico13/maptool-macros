[h, if (argCount() > 0): macroName = arg(0); macroName = "breakpoint"]
[h, if (argCount() > 1): location = arg(1); macroName = "unknown"]
[h: log.debug(macroName + " @ " + location)]
[h, for(i, 2, argCount()): log.debug(i + ": " + if(json.type(arg(i)) == "UNKNOWN", arg(i), json.indent(arg(i))))]
[h: input("ignore|" + location + "|" + macroName + "|TEXT")]