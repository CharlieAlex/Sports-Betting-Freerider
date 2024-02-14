const winChartFormulas = [[
    '=IFERROR(ARRAYFORMULA((E3:E+B3:B+C3:C)/F3:F),"")',
    '=IFERROR(ARRAYFORMULA((E3:E)/F3:F),"")',
    '=ARRAYFORMULA(IF(A3:A<>"", TRUE, FALSE))',
    '=ArrayFormula(MMULT((Transpose((row(B3:B)<=transpose(row(B3:B)))*B3:B)),Sign(B3:B)))',
    '=ArrayFormula(MMULT((Transpose((row(C3:C)<=transpose(row(C3:C)))*C3:C)),Sign(C3:C)))',
    '=ArrayFormula(MMULT((Transpose((row(D3:D)<=transpose(row(D3:D)))*D3:D)),Sign(D3:D)))',
    '=ArrayFormula(MMULT((Transpose((row(E3:E)<=transpose(row(E3:E)))*E3:E)),Sign(E3:E)))',
    '=ArrayFormula(MMULT((Transpose((row(F3:F)<=transpose(row(F3:F)))*F3:F)),Sign(F3:F)))',
    '=iferror(ARRAYFORMULA(IF(I3:I, (M3:M+J3:J+K3:K)/N3:N, "")), "")',
    '=iferror(ARRAYFORMULA(IF(I3:I, (M3:M)/N3:N, "")), "")',
    '=ARRAYFORMULA(IF(I3:I, 57.14%, ""))',
  ]];

const longSheetName = ['total', 'main_push', 'result', 'leaderboard', 'prediction']
