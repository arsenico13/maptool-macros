[h: mapNames = getAllMapNames ()]
[h: mapNamesArry = json.sort (json.fromList (mapNames))]
[h: currentLandingMap = dnd5e_Preferences_getPreference ("landingMapName")]
[h: selectedIndex = json.indexOf (mapNamesArry, currentLandingMap)]
[h, if (selectedIndex < 0): selectedIndex = 0; ""]
[h: abort (input ("landingMapName |" + mapNamesArry + " | Select Landing Map | LIST | delimiter=json value=string select=" + selectedIndex))]
[h: dnd5e_Preferences_setPreference ("landingMapName", landingMapName, 1)]
[g, r: "Landing map has been set to " + landingMapName]
