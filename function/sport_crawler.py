from .config import back_links
import requests
from functools import cached_property
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import re
import json
import pandas as pd
from io import StringIO
import random

user_agent = UserAgent()

class Leaderboard:
    def __init__(self, alliance, during):
        self.web_url = 'https://www.playsport.cc/'
        self.alliance = alliance
        self.during = during
        self.board_url = self.web_url + f'billboard/mainPrediction?during={during}&allianceid={alliance}'
        self.header = {'User-Agent':user_agent.random, 'Referer': random.choice(back_links)}
        self.html_content = BeautifulSoup(self.crawl_content, 'html.parser')

    @cached_property
    def crawl_content(self):
        print('向排行榜發送爬蟲要求!')
        r = requests.get(url=self.board_url, headers=self.header)
        if r.status_code == 403:
            print('IP被ban了, GG...')
        return r.text

    @property
    def board_json(self):
        target_content = self.html_content.find_all('script')[13].string
        results = re.search('var vueData = (\{.*\});', target_content)[1]
        return json.loads(results)

    @property
    def dataframe(self):
        global_ranks = self.board_json['rankers']['1']
        taiwan_ranks = self.board_json['rankers']['2']
        df = pd.DataFrame()
        for i in range(len(global_ranks)):
            df = df._append(global_ranks[i], ignore_index=True)
            df = df._append(taiwan_ranks[i], ignore_index=True)
        df.replace({'mode': {1: '運彩盤賽事', 2: '國際盤賽事'}}, inplace=True)
        df['linkUrl'] = self.web_url + '//' + df['linkUrl']
        return df


class Rank_user:
    def __init__(self, user_data) -> None:
        self.user_data = user_data
        self.header = {'User-Agent':user_agent.random, 'Referer': random.choice(back_links)}
        self.html_content = BeautifulSoup(self.crawl_content, 'html.parser')

    @cached_property
    def crawl_content(self):
        print('向使用者頁面發送爬蟲要求!')
        r = requests.get(url=self.user_data.linkUrl, headers=self.header)
        if r.status_code == 403:
            print('IP被ban了, GG...')
        return r.text

    @property
    def prediction(self)->pd.DataFrame:
        def clean_table(table):
            mode = table.columns[0]
            table = table.iloc[:, 1:-1].copy()
            table.columns = ['game', 'prediction']
            table['userid'] = self.user_data['userid']
            table['nickname'] = self.user_data['nickname']
            table['rank'] = self.user_data['rank']
            table['mode'] = mode
            table = table[table['game'] != '無預測']
            return table[['userid', 'nickname', 'rank', 'mode', 'game', 'prediction']]

        def is_main_push(pred_list):
            main_push_list = []
            for game in range(len(pred_list)):
                str_ = ''.join(str(i) for i in pred_list[game])
                if re.search(r'\b主推\b', str_):
                    main_push_list.append(True)
                else:
                    main_push_list.append(False)
            return main_push_list

        tablebox = pd.DataFrame()
        try:
            tables = pd.read_html(StringIO(self.crawl_content))
            prediction_list = self.html_content.find_all('td', class_='managerpredictcon')
            universe_tablebox, bank_tablebox = pd.DataFrame(), pd.DataFrame()
            for table in tables:
                if table.columns[0] == '國際盤賽事':
                    universe_tablebox = clean_table(table)
                elif table.columns[0] == '運彩盤賽事':
                    bank_tablebox = clean_table(table)
                else:
                    pass
            if universe_tablebox.shape[0] != 0 or bank_tablebox.shape[0] != 0:
                tablebox = pd.concat([universe_tablebox, bank_tablebox], ignore_index=True)
                tablebox['main_push'] = is_main_push(prediction_list)
                print(f'{self.user_data.nickname} 預測蒐集完畢...')
            else:
                tablebox = pd.DataFrame()
                print(f'{self.user_data.nickname} 無免費預測...')
        except Exception as e:
            print(e)
            print(f'未知錯誤請查看{self.user_data.nickname}的網址: {self.user_data.linkUrl}')
        return tablebox

if __name__ == '__main__':
    from .config import alliance_dict
    target = 'NBA'
    during = 'lastmonth'

    rank_list = Leaderboard(alliance_dict[target], during)
    leaderboard = rank_list.dataframe
    print(leaderboard.head())

    all_prediction = pd.DataFrame()
    user = Rank_user(leaderboard.iloc[0])
    all_prediction = pd.concat([all_prediction, user.prediction])
    print(all_prediction.head())