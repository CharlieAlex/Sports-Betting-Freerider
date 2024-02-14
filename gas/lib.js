function getLastNonBlankRow(range){
  let rowNum = 0;
  let blank = false;
  for(let row = 0; row < range.length; row++){
    if(range[row][0] === "" && !blank){
      rowNum = row;
      blank = true;
    }else if(range[row][0] !== ""){
      blank = false;
    };
  };
  return rowNum;
};

function checkCol (checkValues, allowedList) {
  // let ui = SpreadsheetApp.getUi();
  let allowedValues = new Set(allowedList);
  let nonAllowedValues = checkValues.map(function(row) {
    return row[0];
  }).filter(function(value) {
    return !allowedValues.has(value);
  });

  if (nonAllowedValues.length > 0) {
    let wrongColWarning = "欄位有不合理的值存在，請檢查欄位是否正確：" + nonAllowedValues.slice(0, 5).join(', ')
    Logger.log(wrongColWarning);
    // ui.alert(wrongColWarning)
    return false
  } else {
    return true
  }
}

function updateResult(sheetName) {
  function pasteContent (inputCol, formulaCol){
    let formulas = [];
    for (let i = inputRowFrom; i < inputRowTo+1; i++ ) {
      formulas.push([
        '=IFERROR(INDEX(result!' + formulaCol + '$2:' + formulaCol +
        ', MATCH(A' + i + '&B' + i + '&E' + i +
        ', result!A$2:A&result!B$2:B&result!E$2:E, 0)), "")'
      ]);
    }

    let cells = sheet.getRange(inputRowFrom, inputCol, inputRowLength, 1);
    cells.setFormulas(formulas);

    let values = cells.getValues();
    cells.setValues(values);
  }

  let sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName);
  let resultCol = 9, outcomeCol = 10;
  let resultColStr = "H:H", otherColStr = "I:I";

  let maxRow = sheet.getLastRow()
  let inputRowFrom = getLastNonBlankRow(sheet.getRange(otherColStr).getValues())+1;
  let inputRowTo = getLastNonBlankRow(sheet.getRange(resultColStr).getValues());
  let inputRowLength = inputRowTo - inputRowFrom + 1;

  let resultValues = sheet.getRange(3, resultCol, maxRow-3, 1).getValues();
  let outcomeValues = sheet.getRange(3, outcomeCol, maxRow-3, 1).getValues();
  if (!checkCol(resultValues, ["準", "囧", "?", ""]) | !checkCol(outcomeValues, ["準", "囧", "?", ""])) {
    return "欄位有誤，結束此函數"
  }

  pasteContent (resultCol, "C");
  pasteContent (outcomeCol, "D");
}

function addBlankRow(sheetName) {
  let sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName);
  let lastNonBlankRow = getLastNonBlankRow(sheet.getRange("A:A").getValues());
  let maxRow = sheet.getMaxRows();

  if (maxRow - lastNonBlankRow <= 1000){
    sheet.insertRowsAfter(maxRow, 1000);
    Logger.log("Add 1000 rows for " + sheetName);
  } else {
    Logger.log(sheetName + "'s blank rows > 1000");
  }
}