import pygsheets
from pygsheets.worksheet import Worksheet
import datetime
import pandas as pd

def add_datetime(df:pd.DataFrame)->pd.DataFrame:
    df['date'] = datetime.datetime.now().strftime('%Y-%m-%d')
    df['time'] = datetime.datetime.now().strftime('%H:%M:%S')
    return df

def add_sport(df:pd.DataFrame, sport:str)->pd.DataFrame:
    df['sport'] = sport
    return df

def open_gsheet(key_path:str, database_url:str)->(Worksheet, Worksheet):
    sh = (pygsheets
        .authorize(service_account_file=key_path)
        .open_by_url(database_url)
    )
    raw_sheet = sh.worksheet_by_title('rawdata')
    total_sheet = sh.worksheet_by_title('total')
    mainpush_sheet = sh.worksheet_by_title('main_push')
    return raw_sheet, total_sheet, mainpush_sheet

def start_cell(ws:Worksheet)->str:
    df = pd.DataFrame(ws.get_all_values())
    current_rows = df[df[0] != ''].shape[0]
    return "A"+str(current_rows+1)

def append_dataframe(df:pd.DataFrame, ws:Worksheet, sport:str)->None:
    ws.set_dataframe(
        df.pipe(add_datetime).pipe(add_sport, sport),
        start=start_cell(ws), copy_head=False,
    )
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