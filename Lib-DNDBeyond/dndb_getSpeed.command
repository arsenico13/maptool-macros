[h: toon = arg (0)]

[h: speedsMap = json.append ("",
			json.set ("", "name", "Burrow", "verb", "burrowing"),
			json.set ("", "name", "Climb", "verb", "climbing"),
			json.set ("", "name", "Swim", "verb", "swimming"),
			json.set ("", "name", "Walk", "verb", "walking")
			)
]
[h, if (json.length (macro.args) > 1): 
	speedNames = json.append ("", arg(1));
	speedNames = json.append ("", "Burrow", "Climb", "Swim", "Walk")
]

[h: speeds = "[]"]

<!-- Collect base speeds from ractial traits -->
[h: baseSpeeds = json.path.read (toon, "data.race.weightSpeeds.normal")]

<!-- all speeds bonuses -->
[h: allBonuses = dndb_searchGrantedModifiers (json.set ("", 
							"object", toon,
							"property", "value",
							"subType", "speed",
							"type", "bonus"))]
							
[h: log.debug ("allBonuses: " + allBonuses)]

[h: allBonus = 0]
[h, foreach (value, allBonuses): allBonus = allBonus + value]

<!-- Foreach speed type, find all the granted bonuses -->
[h, foreach (speedName, speedNames), code: {
	<!-- I may have to revisit this after some testing, but so far Ive only found -->
	<!-- granted bonuses as setting speeds to innate-speed-swimming, for example. -->
	<!-- So look for those for each speed and well add the allBonus values after -->
	[h: verbSpeed = json.get (dndb_searchJsonObject (json.set ("", "object", speedsMap, "property", "verb", "name", speedName)), 0)]
	[h: innateSpeed = "innate-speed-" + verbSpeed]
	[h: grantedSpeeds = dndb_searchGrantedModifiers (json.set ("", 
							"object", toon,
							"property", "value",
							"type", "set",
							"subType", innateSpeed))]
	[h: log.debug ("grantedSpeeds: " + json.indent (grantedSpeeds))]
	[h: setSpeed = 0]
	[h, if (json.length (grantedSpeeds) > 0), code: {
		<!-- get the biggest one -->
		[h: grantedSpeeds = json.sort (grantedSpeeds, "descending")]
		[h: setSpeed = json.get (grantedSpeeds, 0)]
	}]

	<!-- Find custom speeds and use as overrides -->
	[h: lowerName = lower (speedName)]
	[h: baseSpeed = json.get (baseSpeeds, lowerName)]
	[h: actualSpeed = math.max (baseSpeed, setSpeed)]
	<!-- if actualSpeed is 0, dont apply the allBonus to it -->
	[h, if (actualSpeed > 0): actualSpeed = actualSpeed + allBonus]
	[h: speed = json.set ("", "name", speedName,
						"speed", actualSpeed)]
	[h: speeds = json.append (speeds, speed)]
}]

[h: macro.return = speeds]


<!-- Determine encumberance? Its a variant, so skip for now until we determine -->
<!-- a good way of passing that flag -->