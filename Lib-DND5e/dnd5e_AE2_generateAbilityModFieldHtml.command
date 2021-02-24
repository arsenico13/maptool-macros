[h: l_value = arg(0)]
[h, if (!isNumber(l_value)): l_value = -1]
[h, if (l_value < -1 || l_value > json.length(CHAR_ABILITIES)): l_value = -1]
[h: out = json.append("[]", strformat('<div class="col-3 form-group action-detail%{stepClass}" data-toggle="tooltip" title="Choose an ability modifier to add">'))]
[h: out = json.append(out, strformat('  <label for="%{rowId}-%{ABILITY_MOD_FIELD}-id">Ability Mod:&nbsp;</label>'))]
[h: out = json.append(out, strformat('<select id="%{rowId}-%{ABILITY_MOD_FIELD}-id" name="%{rowId}-%{ABILITY_MOD_FIELD}" class="selectpicker %{stepClass}" title="Choose modifier&hellip;" required>'))]
[h, for(l_index, 0, json.length(CHAR_ABILITIES)), code: {
	[h: ability = json.get(CHAR_ABILITIES, l_index)]
	[h: out = json.append(out, strformat('    <option %s value="%{l_index}">%{ability}</option>', if(l_value == l_index, " selected", "")))]
}]
[h: l_index = json.length(CHAR_ABILITIES)]
[h: out = json.append(out, strformat('    <option %s value="%{l_index}">No modifier</option>', if(l_value == l_index, " selected", "")))]
[h: out = json.append(out, '  </select>')]
[h: out = json.append(out, '</div>')]
[h: log.debug(getMacroName() + " arg(0)= " + arg(0) + " l_value=" + l_value + " out=" + json.indent(out))]
[h: macro.return = json.toList(out, "")]