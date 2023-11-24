from sport_crawler import Leaderboard, Rank_user
from data_process import Output_maker
from config import alliance_dict
import pandas as pd
from tqdm import trange
import time
import random
from datetime import date

target = 'NBA'
during = 'thismonth'
today = date.today().strftime("%Y%m%d")
rawdata_path = '/Users/alexlo/Desktop/Project/Sport_Lottery/rawdata'
workdata_path = '/Users/alexlo/Desktop/Project/Sport_Lottery/workdata'

if __name__ == '__main__':
    #獲得排行榜數據
    rank_list = Leaderboard(alliance_dict[target], during)
    leaderboard = rank_list.dataframe
    leaderboard.to_csv(f'{rawdata_path}/leaderboard_{target}_{today}.csv', index=False)
    leaderboard = leaderboard[leaderboard['mode'] == '國際盤賽事']

    #獲得國際盤排行榜上每一個人的預測數據
    all_prediction = pd.DataFrame()
    crawl_count = 30 if leaderboard.shape[0] > 30 else leaderboard.shape[0]
    collected_count = 0
    for i in trange(crawl_count):
        try:
            user = Rank_user(leaderboard.iloc[i])
            all_prediction = pd.concat([all_prediction, user.prediction])
            collected_count = collected_count + 1 if user.prediction.shape[0] > 0 else collected_count
        except Exception as e:
            print(e)
        if collected_count >= 15:
            break
        time.sleep(random.random()*15)
    all_prediction.to_csv(f'{rawdata_path}/prediction_{target}_{today}.csv', index=False)

    #統計結果
    output = Output_maker(leaderboard, all_prediction)
    output.mainpush_summary.to_csv(f'{workdata_path}/mainpush_{target}_{today}.csv', index=False)
    output.total_summary.to_csv(f'{workdata_path}/total_{target}_{today}.csv', index=False)