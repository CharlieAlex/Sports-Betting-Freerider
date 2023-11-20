import requests
from functools import cached_property
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import re
import json
import pandas as pd
import time
import random
from tqdm import trange

user_agent = UserAgent()
back_links = [
    '','','','','','',
    'https://www.cakeresume.com/companies/playsport-cc',
    'https://mypaper.pchome.com.tw/slk_1320',
    'https://sites.ipaddress.com/playsport.cc/',
    'https://decoratoradvice.com/our-favorite-site-list/',
    'https://ro.wikipedia.org/wiki/Calific%C4%83rile_pentru_Campionatul_Mondial_de_Fotbal_2018_(AFC)_%E2%80%93_prima_rund%C4%83',
    'https://www.juksy.com/article/98898',
    'https://www.jkforum.net/home.php?mod=space&uid=3545071',
    'https://tw.pycon.org/2018/zh-hant/events/talk/596319992962613435/',
]

class Leaderboard:
    def __init__(self):
        self.web_url = 'https://www.playsport.cc/'
        self.sport_time = 'lastmonth'
        self.alliance = '3'
        self.header = {'User-Agent':user_agent.random, 'Referer': random.choice(back_links)}
        self.html_content = BeautifulSoup(self.crawl_content, 'html.parser')

    @property
    def list_url(self):
        return self.web_url + f'billboard/mainPrediction?during={self.sport_time}&allianceid={self.alliance}'

    @cached_property
    def crawl_content(self):
        print('Crawling!')
        return requests.get(url=self.list_url, headers=self.header).text

    @property
    def list_json(self):
        target_content = self.html_content.find_all('script')[13].string
        results = re.search('var vueData = (\{.*\});', target_content)[1]
        return json.loads(results)

    @property
    def intl_list_json(self):
        return self.list_json['rankers']['1']

    @property
    def lot_list_json(self):
        return self.list_json['rankers']['2']

    @property
    def dataframe(self):
        df = pd.DataFrame()
        for i in range(len(self.intl_list_json)):
            df = df._append(self.intl_list_json[i], ignore_index=True)
            df = df._append(self.lot_list_json[i], ignore_index=True)
        df['linkUrl'] = self.web_url + '//' + df['linkUrl']
        return df

class Rank_user:
    def __init__(self, user_data) -> None:
        self.user_data = user_data
        self.header = {'User-Agent':user_agent.random, 'Referer': random.choice(back_links)}
        self.html_content = BeautifulSoup(self.crawl_content, 'html.parser')

    @cached_property
    def crawl_content(self):
        print('發送爬蟲要求!')
        return requests.get(url=self.user_data.linkUrl, headers=self.header).text

    @property
    def prediction1(self)->pd.DataFrame:
        game_list = self.html_content.find_all('td', class_='index-prediction-game')
        pred_list = self.html_content.find_all('td', class_='index-prediction-team')

        df = pd.DataFrame()
        for i in range(len(game_list)):
            team1 = game_list[i].text.split('VS')[0].strip()
            team2 = game_list[i].text.split('VS')[1].strip()
            win_team = pred_list[i].contents[0].strip()
            win_pred = pred_list[i].contents[1].text
            df = df._append({
                'team1': team1,
                'team2': team2,
                'win_team': win_team,
                'win_prediction': win_pred
                }, ignore_index=True)
        return df

    @property
    def prediction2(self)->pd.DataFrame:
        game_list = self.html_content.find_all('td', rowspan='1')[1::2]
        pred_list = self.html_content.find_all('td', class_='managerpredictcon')

        df = pd.DataFrame()
        try:
            for i in range(len(pred_list)):
                team1 = game_list[i].find_all('th')[0].text.strip()
                team2 = game_list[i].find_all('th')[1].text.strip()
                win_team = pred_list[i].contents[0].strip()
                win_pred = pred_list[i].contents[1].text
                df = df._append({
                    'userid': self.user_data.userid,
                    'nickname': self.user_data.nickname,
                    'team1': team1,
                    'team2': team2,
                    'win_team': win_team,
                    'win_prediction': win_pred,
                    }, ignore_index=True)
        except IndexError:
            print(f': {self.user_data.userid} 無免費預測...')
        except Exception as e:
            print(e)
            print(f'請查看以下網址: {self.user_data.linkUrl}!')
        return df

if __name__ == '__main__':
    rank_list = Leaderboard()
    df = rank_list.dataframe
    df.to_csv('rank_list.csv', index=False)
    df_url = df[['userid', 'nickname', 'linkUrl']]

    all_prediction = pd.DataFrame()
    crawl_count = 20 if df_url.shape[0] > 20 else df_url.shape[0]
    for i in trange(crawl_count):
        user = Rank_user(df_url.iloc[i])
        all_prediction = pd.concat([all_prediction, user.prediction2])
        time.sleep(random.random()*5)
    all_prediction.to_csv('all_prediction.csv', index=False)