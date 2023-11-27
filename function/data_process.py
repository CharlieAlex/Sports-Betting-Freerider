import pandas as pd

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
        return (df[['game', 'prediction', 'count']]
            .groupby(['game', 'prediction']).count()
            .sort_values(['count'], ascending=False)
            .reset_index()
            )

    @property
    def total_summary(self):
        df = self.merge_df[self.is_mode].copy()
        df['count'] = 1
        df['game'] = (df['game']
            .str.replace(r'\s*\d+\s*分[贏輸]\d+%?\s*', '', regex=True)
            .str.strip()
            .replace('無預測', pd.NA)
            )
        df['prediction'] = (df['prediction']
            .str.replace(r'\d.|[贏輸%]', '', regex=True)
            .str.strip()
            )
        return (df[['game', 'prediction', 'count']]
            .groupby(['game', 'prediction']).count()
            .sort_values(['count'], ascending=False)
            .reset_index()
            )

if __name__ == '__main__':
    import os
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