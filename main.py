from function import gmail as gm
from function import sport_crawler as sc
from function import data_process as dp
from function import gsheet as gs
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
from google.cloud import bigquery
from gcp import schema


def main(target, during, target_num, is_gc):
    # 獲得排行榜數據
    if re.match(r"^yesterday|.*daysAgo$", during):
        gameday, during = during, "lastmonth"
    else:
        gameday = "today"
    leaderboard = pd.DataFrame()
    for page in range(2):
        try:
            rank_list = sc.Leaderboard(alliance_dict[target], during, page, gameday)
            tempboard = rank_list.dataframe
            tempboard = tempboard[tempboard["mode"] == "國際盤賽事"]
            leaderboard = pd.concat([leaderboard, tempboard], ignore_index=True)
        except Exception as e:
            print(e)

    # 獲得國際盤排行榜上每一個人的預測數據
    all_prediction = pd.DataFrame()
    crawl_num = leaderboard.shape[0]
    collected_count = 0
    for i in trange(crawl_num):
        try:
            user = sc.Rank_user(leaderboard.iloc[i])
            all_prediction = pd.concat([all_prediction, user.prediction])
            collected_count = (
                collected_count + 1 if user.prediction.shape[0] > 0 else collected_count
            )
        except Exception as e:
            print(e)
        if collected_count >= int(target_num):
            break
        if is_gc:
            gc.collect()
        time.sleep(random.random() * 5)

    return leaderboard, all_prediction


def result_main(target, during, target_num, is_gc, gs_key, bq_key):
    leaderboard, prediction = main(target, during, target_num, is_gc)
    print("爬蟲完畢")

    output = dp.Output_maker(leaderboard, prediction)
    data = {"result": output.result_summary}
    deltadays = sc.parse_during(during)
    df = (
        data["result"]
        .pipe(gs.add_datetime, deltadays)
        .pipe(gs.add_sport, target)
        .pipe(gs.add_during, during)
        .pipe(gs.sort_result)
        .pipe(gs.drop_NA)
    )
    print("資料整理完畢")

    sh = gs.pygsheets.authorize(service_account_file=gs_key).open_by_url(database_url)
    result_sheet = sh.worksheet_by_title("result")
    result_sheet.set_dataframe(df, start=gs.start_cell(result_sheet), copy_head=False)
    print("資料上傳至 Google Sheet")

    client = bigquery.Client.from_service_account_json(json_credentials_path=bq_key)
    client.load_table_from_dataframe(
        df,
        "sport-lottery-database.playsports.result",
        job_config=schema.set_job_config(schema.result_schema),
    ).result()
    print("資料上傳至 Google Cloud")

    return None


def enter_command():
    command_text = input("請輸入指令開始爬蟲(e.g. NBA thismonth 15):")
    try:
        command_list = command_text.split()
        return command_list[0], command_list[1], int(command_list[2])
    except Exception as e:
        print(e)
        return None, None, None


if __name__ == "__main__":
    # NBA season 3
    load_dotenv("/Users/alexlo/Desktop/Project/Others/App_Setting/.env")
    gs_key = "/Users/alexlo/Desktop/Project/Sport_Lottery/g-sheet.json"
    bq_key = "/Users/alexlo/Desktop/Project/Sport_Lottery/big-query.json"

    # 蒐集資料
    target, during, target_num = enter_command()
    print("開始爬蟲!")
    if during is not None and re.match(r"^yesterday|.*daysAgo$", during):
        result_main(
            target, during, target_num, is_gc=False, gs_key=gs_key, bq_key=bq_key
        )
    else:
        taipei_timezone = pytz.timezone("Asia/Taipei")
        today = datetime.now(taipei_timezone).strftime("%Y%m%d")
        leaderboard, prediction = main(target, during, target_num, is_gc=False)
        leaderboard.to_csv(
            f"{rawdata_path}/leaderboard_{target}_{today}.csv", index=False
        )
        prediction.to_csv(
            f"{rawdata_path}/prediction_{target}_{today}.csv", index=False
        )
        print("爬蟲完畢")

        # 統計結果
        output = dp.Output_maker(leaderboard, prediction)
        output.mainpush_summary.to_csv(
            f"{workdata_path}/mainpush_{target}_{today}.csv", index=False
        )
        output.total_summary.to_csv(
            f"{workdata_path}/total_{target}_{today}.csv", index=False
        )
        data = {
            "leaderboard": leaderboard,
            "prediction": prediction,
            "mainpush": output.mainpush_summary,
            "total": output.total_summary,
        }

        # 寄送郵件
        gmail_machine = gm.Gmail_machine(target, today, data)
        gmail_machine.send_mail(os.getenv("Alex_Account"))
        print("寄送郵件完畢!")
