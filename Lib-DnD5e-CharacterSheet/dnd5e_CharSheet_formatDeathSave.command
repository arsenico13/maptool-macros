[h: isSuccess = arg (0)]
[h: whichSave = arg (1)]
[h: savesFailed = getProperty ("DSFail")]
[h, if (!isNumber (savesFailed)): savesFailed = 0]
[h: savesPassed = getProperty ("DSPass")]
[h, if (!isNumber (savesPassed)): savesPassed = 0]
[h: retChar = "O"]
[h, if (isSuccess && whichSave <= savesPassed): retChar = "&check;"]
[h, if (!isSuccess && whichSave <= savesFailed): retChar = "X"]
[r: retChar]