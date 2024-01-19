import pygsheets
from pygsheets.worksheet import Worksheet
from datetime import datetime, timedelta
import pandas as pd
import pytz

def add_datetime(df:pd.DataFrame, deltadays:int|str)->pd.DataFrame:
    taipei_timezone = pytz.timezone('Asia/Taipei')
    now = datetime.now(taipei_timezone)
    assign_date = now - timedelta(days=int(deltadays))
    df['date'] = assign_date.strftime('%Y-%m-%d')
    df['time'] = assign_date.strftime('%H:%M:%S')
    return df

def add_sport(df:pd.DataFrame, sport:str)->pd.DataFrame:
    df['sport'] = sport
    return df

def add_during(df:pd.DataFrame, during:str)->pd.DataFrame:
    df['during'] = during
    return df

def add_rank(df:pd.DataFrame)->pd.DataFrame:
    df['rank']  = df['count'].rank(ascending=False, method='min')
    return df

def sort_result(df:pd.DataFrame)->pd.DataFrame:
    df = df.sort_values(
        ['date', 'time', 'game', 'prediction'],
        ascending=[True, True, True, False],
    )
    return df

def open_gsheet(key_path:str, database_url:str)->(Worksheet, Worksheet):
    sh = (pygsheets
        .authorize(service_account_file=key_path)
        .open_by_url(database_url)
    )
    board_sheet = sh.worksheet_by_title('leaderboard')
    pred_sheet = sh.worksheet_by_title('prediction')
    total_sheet = sh.worksheet_by_title('total')
    mainpush_sheet = sh.worksheet_by_title('main_push')
    return board_sheet, pred_sheet, total_sheet, mainpush_sheet

def start_cell(ws:Worksheet)->str:
    df = pd.DataFrame(ws.get_all_values())
    current_rows = df[df[0] != ''].shape[0]
    return "A"+str(current_rows+1)

def append_dataframe(df:pd.DataFrame, ws:Worksheet, sport:str, during:str)->None:
    df = (df
        .pipe(add_datetime, 0)
        .pipe(add_sport, sport)
        .pipe(add_during, during)
    )
    ws.set_dataframe(df, start=start_cell(ws), copy_head=False)
    return None

if __name__ == '__main__':
    key_path = '/Users/alexlo/Desktop/Project/Sport_Lottery/sport-lottery-database-a36862122f3a.json'
    database_url = 'https://docs.google.com/spreadsheets/d/1IcTCgwnIk_EKnqRdBYK7-MGfxiTrxbTnm3-89Fc76X4/edit?usp=sharing'

    target = 'NBA'
    df = pd.read_csv('/Users/alexlo/Desktop/Project/Sport_Lottery/rawdata/prediction_NBA_20231207.csv')
    raw_sheet, total_sheet, mainpush_sheet = open_gsheet(key_path, database_url)
    append_dataframe(df, raw_sheet, target)
    append_dataframe(df, mainpush_sheet, target)
    append_dataframe(df, total_sheet, target)