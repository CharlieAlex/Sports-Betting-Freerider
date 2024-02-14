function updateWinChart() {
  let sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("win_chart");
  let startCol = 7, endCol = 17;
  let lengthCol = endCol-startCol+1
  let maxRow = sheet.getMaxRows();
  let formula_range = sheet.getRange(3, startCol, 1, lengthCol);
  let values_range = sheet.getRange(3, startCol, maxRow, lengthCol);
  values_range.clearContent();

  formula_range.setFormulas(winChartFormulas);
  let values = values_range.getValues();
  values_range.setValues(values);
}

function updateBlankRow(){
  for (var sheetName of longSheetName) {
    addBlankRow(sheetName);
  }
}

function update_total() {
  updateResult("total")
}

function update_main() {
  updateResult("main_push")
}

function onOpen(e) {
  SpreadsheetApp.getUi()
    .createMenu('專案選單')
    .addItem('更新win_chart', 'updateWinChart')
    .addItem('更新total', 'update_total')
    .addItem('更新main', 'update_main')
    .addItem('更新空白列', 'updateBlankRow')
    .addToUi();
}


