from config import alliance_dict, back_links
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
    def __init__(self, during, alliance):
        self.web_url = 'https://www.playsport.cc/'
        self.during = during
        self.alliance = alliance
        self.header = {'User-Agent':user_agent.random, 'Referer': random.choice(back_links)}
        self.html_content = BeautifulSoup(self.crawl_content, 'html.parser')

    @property
    def list_url(self):
        return self.web_url + f'billboard/mainPrediction?during={self.during}&allianceid={self.alliance}'

    @cached_property
    def crawl_content(self):
        print('向排行榜發送爬蟲要求!')
        return requests.get(url=self.list_url, headers=self.header).text

    @property
    def list_json(self):
        target_content = self.html_content.find_all('script')[13].string
        results = re.search('var vueData = (\{.*\});', target_content)[1]
        return json.loads(results)

    @property
    def global_ranks(self):
        return self.list_json['rankers']['1']

    @property
    def taiwan_ranks(self):
        return self.list_json['rankers']['2']

    @property
    def dataframe(self):
        df = pd.DataFrame()
        for i in range(len(self.global_ranks)):
            df = df._append(self.global_ranks[i], ignore_index=True)
            df = df._append(self.taiwan_ranks[i], ignore_index=True)
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
        return requests.get(url=self.user_data.linkUrl, headers=self.header).text

    def is_main_push(self, ls:list):
        str_ = ''.join(str(i) for i in ls)
        if re.search(r'\b主推\b', str_):
            return True
        else:
            return False

    def compute_game_mode(self, i:int, pred_num:int, game_mode:list):
        if len(game_mode) == 1:
            return game_mode[0]
        else:
            if i < pred_num/2:
                return game_mode[0]
            else:
                return game_mode[1]

    @property
    def prediction(self)->pd.DataFrame:
        is_paid = self.html_content.find('a', class_='buypredictbt iframe')
        game_list = self.html_content.find_all('td', rowspan='1')[1::2]
        pred_list = self.html_content.find_all('td', class_='managerpredictcon')
        pred_num = len(game_list)
        game_mode_list = [i.text for i in self.html_content.find_all('th', {'class': 'gameevent'})]
        df = pd.DataFrame()

        if is_paid:
            print(f'{self.user_data.userid} 無免費預測...')
            return df
        else:
            try:
                for i in range(pred_num):
                    team1 = game_list[i].find_all('th')[0].text.strip()
                    team2 = game_list[i].find_all('th')[1].text.strip()
                    win_team = pred_list[i].contents[0].strip()
                    win_pred = pred_list[i].contents[1].text
                    main_push = self.is_main_push(pred_list[i])
                    game_mode = self.compute_game_mode(i, pred_num, game_mode_list)
                    df = df._append({
                        'userid': self.user_data.userid,
                        'nickname': self.user_data.nickname,
                        'team1': team1,
                        'team2': team2,
                        'win_team': win_team,
                        'win_prediction': win_pred,
                        'main_push': main_push,
                        'game_mode': game_mode,
                        }, ignore_index=True)
                print(f'{self.user_data.userid} 預測蒐集完畢...')
            except Exception as e:
                print(e)
                print(f'未知錯誤請查看此人網址: {self.user_data.linkUrl}')
            return df

if __name__ == '__main__':
    from datetime import date

    target = 'NBA'
    during = 'lastmonth'
    today = date.today().strftime("%Y%m%d")
    rawdata_path = '/Users/alexlo/Desktop/Project/Sport_Lottery/rawdata'

    rank_list = Leaderboard(during, alliance_dict[target])
    leaderboard = rank_list.dataframe
    print(leaderboard.head())

    all_prediction = pd.DataFrame()
    user = Rank_user(leaderboard.iloc[10])
    all_prediction = pd.concat([all_prediction, user.prediction])
    print(all_prediction.head())