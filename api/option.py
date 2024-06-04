import datetime

table_options = {
    "所有預測": "total_result",
    "主推預測": "mainpush_result",
}

sport_options = [
    "NBA",
    "MLB",
    "日本職棒",
    "NHL冰球",
]

ranktime_options = [
    "lastmonth",
    "thismonth",
]


today = datetime.date.today()
start_of_month = today.replace(day=1)
