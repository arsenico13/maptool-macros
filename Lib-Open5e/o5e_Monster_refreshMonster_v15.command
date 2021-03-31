[h: o5e_Constants (getMacroName())]
[h: isOldVersion = dnd5e_Util_checkVersion (getProperty (PROP_MONSTER_TOON_VERSION), "0.16")]
[h: assert (!isOldVersion, getName() + ": Does not require refresh")]
[h: slug = getProperty ("Character ID")]
[h: monsterToon = o5e_Open5e_get ("monsters/" + slug)]
[h: setProperty (PROP_MONSTER_TOON_JSON, monsterToon)]
[h: CRString = json.get (monsterToon, "challenge_rating")]
[h, if (CRString == ""): CRString = "0"]
[h: evalMacro ("[h: CR = " + CRString + "]")]
[h: Proficiency = floor(math.max (0, CR - 1) / 4) + 2]
[h: o5e_Token_Monster_applySpecialAbilities (monsterToon)]
[h: o5e_Token_Monster_applyActions (monsterToon)]
[h: setProperty (PROP_MONSTER_TOON_VERSION, "0.16")]