import requests
from bs4 import BeautifulSoup
import re
import json
import pandas as pd

class Leaderboard:
    def __init__(self):
        self.web_url = 'https://www.playsport.cc/'
        self.sport_time = 'lastmonth'
        self.alliance = '3'

    @property
    def list_url(self):
        return self.web_url + f'billboard/mainPrediction?during={self.sport_time}&allianceid={self.alliance}'

    @property
    def list_json(self):
        r = requests.get(url=self.list_url)
        html_content = BeautifulSoup(r.text, 'html.parser')
        target_content = html_content.find_all('script')[13].string
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
    def __init__(self, url) -> None:
        self.url = url
        self.html_content = BeautifulSoup(requests.get(url).text, 'html.parser')

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
        pred_list = self.find_all('td', class_='managerpredictcon')

        df = pd.DataFrame()
        for i in range(len(pred_list)):
            team1 = game_list[i].find_all('th')[0].text.strip()
            team2 = game_list[i].find_all('th')[1].text.strip()
            win_team = pred_list[i].contents[0].strip()
            win_pred = pred_list[i].contents[1].text
            df = df._append({
                'team1': team1,
                'team2': team2,
                'win_team': win_team,
                'win_prediction': win_pred
                }, ignore_index=True)
        return df

if __name__ == '__main__':
    rank_list = Leaderboard()
    df = rank_list.dataframe
    df_url = df[['nickname', 'linkUrl']]

    all_prediction = pd.DataFrame()
    for i in df_url.shape[0]:
        user = Rank_user(df_url.iloc[i].linkUrl)
        all_prediction = pd.concat([all_prediction, user.prediction2])