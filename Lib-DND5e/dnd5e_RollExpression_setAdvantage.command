[h: rollExpression = arg (0)]
[h, if (!dnd5e_RollExpression_hasType (rollExpression, "advantagable")): rollExpression = dnd5e_RollExpression_addType (rollExpression, dnd5e_Type_Advantagable()); ""]
[h: log.debug (getMacroName() + ": rollExpression = " + rollExpression)]
[h: macro.return = json.set (rollExpression, "hasAdvantage", arg (1))]