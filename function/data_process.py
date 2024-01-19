import pandas as pd
from function.config import team_pattern

class Output_maker:
    def __init__(self, leaderboard, prediction) -> None:
        self.leaderboard = leaderboard
        self.prediction_df = prediction
        self.merge_df = pd.merge(self.leaderboard_df, self.prediction_df, on='userid', how='inner')
        self.is_mainpush = (self.merge_df['main_push']==True)
        self.is_mode = (self.merge_df['mode_x']==self.merge_df['mode_y'])

    @property
    def leaderboard_df(self):
        df = self.leaderboard[['userid', 'wingame', 'losegame', 'winpercentage', 'mode', 'winearn', 'rank']]
        df = df[df['mode'] == '國際盤賽事'].reset_index(drop=True)
        return df

    def combine_game(self, df:pd.DataFrame)->pd.DataFrame:
        df['game_origin'] = (df['game']
            .str.replace(r'\s*\d+\s*分[贏輸]\d+%?\s*', '', regex=True)
            .str.strip()
            .replace('無預測', pd.NA)
        )
        df['game'] = (df['game_origin']
            .str.replace('(主)', '')
            .str.extract(f'(?P<guest_team>{team_pattern})\s*(?P<home_team>{team_pattern})')
            .assign(game = lambda x: x['guest_team'] + ' vs ' + x['home_team'])
            .drop(['guest_team', 'home_team'], axis=1)
            )
        return df

    def fix_team_name(self, df:pd.DataFrame)->pd.DataFrame:
        df = (df
            .str.replace('費城人', '費城76人')
            .str.replace('阿德雷德人', '阿德雷德36人')
        )
        return df

    def combine_prediction(self, df:pd.DataFrame)->pd.DataFrame:
        df['prediction'] = (df['prediction']
            .str.replace(r'\d.|[贏輸%]', '', regex=True)
            .str.strip()
            .pipe(self.fix_team_name)
            )
        return df

    def count_prediction(self, df:pd.DataFrame)->pd.DataFrame:
        df['count'] = 1
        return (df[['game', 'prediction', 'count']]
            .groupby(['game', 'prediction']).count()
            .sort_values(['count'], ascending=False)
            .reset_index()
            )

    def drop_duplicate(self, df:pd.DataFrame)->pd.DataFrame:
        return df[['game', 'prediction', 'result']].drop_duplicates()

    def drop_score(self, df:pd.DataFrame)->pd.DataFrame:
        df['game'] = df['game'].str.replace(r'^\d+\s*V\.S\.\s*\d+\s*', '', regex=True)
        return df

    @property
    def mainpush_summary(self):
        df = self.merge_df[self.is_mode & self.is_mainpush].copy()
        return (df
            .pipe(self.combine_game)
            .pipe(self.combine_prediction)
            .pipe(self.count_prediction)
            )

    @property
    def total_summary(self):
        df = self.merge_df[self.is_mode].copy()
        return (df
            .pipe(self.combine_game)
            .pipe(self.combine_prediction)
            .pipe(self.count_prediction)
            )

    @property
    def result_summary(self):
        df = self.merge_df[self.is_mode].copy()
        return (df
            .pipe(self.combine_game)
            .pipe(self.combine_prediction)
            .pipe(self.drop_duplicate)
            .pipe(self.drop_score)
            .pipe(self.extend_result)
            )

    def extend_result(self, df:pd.DataFrame)->pd.DataFrame:
        def switch_result(df:pd.DataFrame, res:[str])->pd.DataFrame:
            return df.replace({res[0]:res[1], res[1]:res[0]})
        def switch_pred_team(row:pd.DataFrame):
            temp = (row['pred_team'] == row['guest_team'])
            row['pred_team'] = row['home_team'] if temp else row['guest_team']
            return row

        is_totalover = df['prediction'].isin(['大分', '小分'])
        df_over, df_win = df[is_totalover], df[~is_totalover]
        teams = df_win['game'].str.split(' vs ', expand=True)
        preds = df_win['prediction'].str.split(' ', expand=True)

        df_over = pd.concat([
            df_over.copy(),
            df_over.copy()
                .pipe(switch_result, ['大分', '小分'])
                .pipe(switch_result, ['準', '囧'])
        ])
        df_win = pd.concat([
            df_win.copy(),
            df_win.copy()
                .assign(pred_team=preds[0], pred_text=preds[1], guest_team=teams[0], home_team=teams[1])
                .pipe(switch_result, ['準', '囧'])
                .pipe(switch_result, ['讓分', '受讓'])
                .apply(switch_pred_team, axis=1)
                .assign(prediction=lambda x: x['pred_team'] + ' ' + x['pred_text'])
                .drop(['pred_team', 'pred_text', 'guest_team', 'home_team'], axis=1)
        ])

        return pd.concat([df_over, df_win]).drop_duplicates()


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