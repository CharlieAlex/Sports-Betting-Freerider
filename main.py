from function.sport_crawler import Leaderboard, Rank_user
from function.data_process import Output_maker
from function.gmail import Gmail_machine
from function.gsheet import *
from function.config import rawdata_path, workdata_path, database_url, alliance_dict
import os
import re
from dotenv import load_dotenv
import pandas as pd
from tqdm import trange
import time
import random
from datetime import datetime
import pytz
import gc

def main(target, during, target_num, is_gc):
    #獲得排行榜數據
    if re.match(r'^yesterday|.*daysAgo$', during):
        gameday, during = during, 'thismonth'
    else:
        gameday = 'today'
    rank_list = Leaderboard(alliance_dict[target], during, gameday)
    leaderboard = rank_list.dataframe
    leaderboard = leaderboard[leaderboard['mode'] == '國際盤賽事']

    #獲得國際盤排行榜上每一個人的預測數據
    all_prediction = pd.DataFrame()
    crawl_num = 30 if leaderboard.shape[0] > 30 else leaderboard.shape[0]
    collected_count = 0
    for i in trange(crawl_num):
        try:
            user = Rank_user(leaderboard.iloc[i])
            all_prediction = pd.concat([all_prediction, user.prediction])
            collected_count = collected_count + 1 if user.prediction.shape[0] > 0 else collected_count
        except Exception as e:
            print(e)
        if collected_count >= int(target_num):
            break
        if is_gc:
            gc.collect()
        time.sleep(random.random()*5)

    return leaderboard, all_prediction

def result_main(target, during, target_num, is_gc, key_path):
    leaderboard, prediction = main(target, during, target_num, is_gc)
    print('爬蟲完畢')

    output = Output_maker(leaderboard, prediction)
    data = {'result': output.result_summary}
    print('資料整理完畢')

    sh = (pygsheets
        .authorize(service_account_file=key_path)
        .open_by_url(database_url)
    )
    result_sheet = sh.worksheet_by_title('result')
    deltadays = 1 if re.match(r'^yesterday$', during) else int(re.search(r'\d+', during)[0])
    df = (data['result']
        .pipe(add_datetime, deltadays)
        .pipe(add_sport, target)
        .pipe(add_during, during)
    )
    result_sheet.set_dataframe(df, start=start_cell(result_sheet), copy_head=False)
    print('資料儲存完畢')

    return None

def enter_command():
    command_text = input('請輸入指令開始爬蟲(e.g. NBA thismonth 15):')
    try:
        command_list = command_text.split()
        return command_list[0], command_list[1], int(command_list[2])
    except Exception as e:
        print(e)
        return None, None, None


if __name__ == '__main__':
    # NBA season 3
    load_dotenv('/Users/alexlo/Desktop/Project/Others/App_Setting/.env')
    key_path_local = '/Users/alexlo/Desktop/Project/Sport_Lottery/sport-lottery-database-a36862122f3a.json'

    #蒐集資料
    target, during, target_num = enter_command()
    print('開始爬蟲!')
    if re.match(r'^yesterday|.*daysAgo$', during):
        result_main(target, during, target_num, is_gc=True, key_path=key_path_local)
    else:
        taipei_timezone = pytz.timezone('Asia/Taipei')
        today = datetime.now(taipei_timezone).strftime('%Y%m%d')
        leaderboard, prediction = main(target, during, target_num, is_gc=False)
        leaderboard.to_csv(f'{rawdata_path}/leaderboard_{target}_{today}.csv', index=False)
        prediction.to_csv(f'{rawdata_path}/prediction_{target}_{today}.csv', index=False)
        print('爬蟲完畢')

        #統計結果
        output = Output_maker(leaderboard, prediction)
        output.mainpush_summary.to_csv(f'{workdata_path}/mainpush_{target}_{today}.csv', index=False)
        output.total_summary.to_csv(f'{workdata_path}/total_{target}_{today}.csv', index=False)
        data = {
            'leaderboard': leaderboard,
            'prediction': prediction,
            'mainpush': output.mainpush_summary,
            'total': output.total_summary
        }

        #寄送郵件
        gmail_machine = Gmail_machine(target, today, data)
        gmail_machine.send_mail(os.getenv('Alex_Account'))
        print('寄送郵件完畢!')

        #儲存資料
        board_sheet, pred_sheet, total_sheet, mainpush_sheet = open_gsheet(
            key_path=key_path_local,
            database_url=database_url,
        )
        append_dataframe(data['leaderboard'], board_sheet, target, during)
        append_dataframe(data['prediction'], pred_sheet, target, during)
        append_dataframe(data['mainpush'].pipe(add_rank), mainpush_sheet, target, during)
        append_dataframe(data['total'].pipe(add_rank), total_sheet, target, during)
        print('資料儲存完畢')