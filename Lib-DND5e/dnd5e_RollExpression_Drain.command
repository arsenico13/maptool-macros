[h, if (argCount() > 0): name = arg (0); name = ""]
[h: rollExpression = dnd5e_RollExpression_setName ("", name)]
[h: rollExpression = dnd5e_RollExpression_setExpressionType (rollExpression, "Drain")]
[h: rollExpression = dnd5e_RollExpression_addType (rollExpression, dnd5e_Type_Basic(), dnd5e_Type_Damageable())]
[h, if (argCount() > 1): rollExpression = dnd5e_RollExpression_parseRoll(rollExpression, arg(1))]
[h: macro.return = rollExpression]