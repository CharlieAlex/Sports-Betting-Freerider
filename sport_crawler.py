import requests
from bs4 import BeautifulSoup
import re
import json

class Rank_list:
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

    def get_rankuser_url(self, json_data):
        list_ = []
        for i in range(len(json_data)):
            user_url = self.web_url + '//' + json_data[i]['linkUrl']
            list_.append(user_url)
        return list_

class Rank_user:
    def __init__(self, url) -> None:
        self.url = url
        self.html_content = BeautifulSoup(requests.get(url).text, 'html.parser')

    @property
    def prediction_game(self):
        return self.html_content.find_all('td', class_='index-prediction-game')


if __name__ == '__main__':
    rank_list = Rank_list()
    url_list = rank_list.get_rankuser_url(rank_list.intl_list_json)
    print(Rank_user(url_list[2]).prediction_game[0])