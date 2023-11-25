import os
import pandas as pd
import re

class Output_maker:
    def __init__(self, leaderboard, prediction) -> None:
        self.leaderboard = leaderboard
        self.prediction_df = prediction
        self.merge_df = pd.merge(self.leaderboard_df, prediction, on='userid', how='inner')
        self.is_mainpush = (self.merge_df['main_push']==True)
        self.is_mode = (self.merge_df['mode_x']==self.merge_df['mode_y'])

    @property
    def leaderboard_df(self):
        df = self.leaderboard[['userid', 'wingame', 'losegame', 'winpercentage', 'mode', 'winearn', 'rank']]
        df = df[df['mode'] == '國際盤賽事'].reset_index(drop=True)
        return df

    @property
    def mainpush_summary(self):
        df = self.merge_df[self.is_mode & self.is_mainpush].copy()
        df['count'] = 1
        df = df.groupby(['game', 'prediction'])[['count']].count().reset_index()
        return df

    @property
    def total_summary(self):
        df = self.merge_df[self.is_mode].copy()
        df['count'] = 1
        df['game'] = df['game'].str.replace(r'\s*\d+\s*分[贏輸]\d+%?\s*', '', regex=True)
        df['prediction'] = df['prediction'].apply(lambda x: re.sub(r'\d.', '', x))
        df['prediction'] = df['prediction'].apply(lambda x: re.sub(r'[贏輸]%', '', x))
        df = df.groupby(['game', 'prediction'])[['count']].count().sort_values(['count'], ascending=False).reset_index()
        df = df[df['game'] != '無預測']
        return df

if __name__ == '__main__':
    from datetime import date
    from config import rawdata_path, workdata_path
    target = 'NBA'
    today = date.today().strftime("%Y%m%d")

    os.chdir(rawdata_path)
    prediction = pd.read_csv('prediction_NBA_20231125.csv')
    leaderboard = pd.read_csv('leaderboard_NBA_20231125.csv')

    output = Output_maker(leaderboard, prediction)
    output.mainpush_summary.to_csv(f'{workdata_path}/mainpush_{target}_{today}.csv', index=False)
    output.total_summary.to_csv(f'{workdata_path}/total_{target}_{today}.csv', index=False)