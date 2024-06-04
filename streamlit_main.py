# streamlit run streamlit_main.py
import streamlit as st
from api import helper, option
from gcp import query_bq_table
from google.cloud import bigquery as bq
import datetime as dt
from dateutil import relativedelta as dtr

# streamlit setting & GCP setting & load data
st.set_page_config(
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.title("Sports-Betting-Freerider")
helper.make_bq_key()
bq_key = "/Users/alexlo/Desktop/Project/Sport_Lottery/bq-key.json"
client = bq.Client.from_service_account_json(json_credentials_path=bq_key)
rawdf = query_bq_table.load_data(client, helper.all_3months_query)


# dashboard
today = dt.datetime.today().date()
current_month_1stday = today.replace(day=1)
last_month_sameday = today - dtr.relativedelta(months=1)
last_month_1stday = (current_month_1stday - dt.timedelta(days=1)).replace(day=1)

current_month_ture_ratio = helper.true_ratio(rawdf, current_month_1stday, today)
last_month_ture_ratio = helper.true_ratio(rawdf, last_month_1stday, last_month_sameday)
delta_true_ratio = round(current_month_ture_ratio - last_month_ture_ratio, 2)

current_month_count = helper.pred_count(rawdf, current_month_1stday, today)
last_month_count = helper.pred_count(rawdf, last_month_1stday, last_month_sameday)
delta_count = current_month_count - last_month_count

current_month_NAcount = helper.na_count(rawdf, current_month_1stday, today)
last_month_NAcount = helper.na_count(rawdf, last_month_1stday, last_month_sameday)
delta_NAcount = current_month_NAcount - last_month_NAcount

thismonth_overall_performance = helper.hist_overall_outcome(rawdf, "thismonth")
lastmonth_overall_performance = helper.hist_overall_outcome(rawdf, "lastmonth")

das1, das2, das3 = st.columns(3)
das1.metric("當月正確率", f"{current_month_ture_ratio}%", f"{delta_true_ratio}%")
das2.metric("當月預測數量", f"{current_month_count}", f"{delta_count}")
das3.metric("當月錯誤數量", f"{current_month_NAcount}", f"{delta_NAcount}")

das4, das5 = st.columns(2)
das4.plotly_chart(lastmonth_overall_performance, use_container_width=True)
das5.plotly_chart(thismonth_overall_performance, use_container_width=True)


# input options
with st.form(key="submit"):
    table_id, start_date, end_date = str(), str(), str()
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        # choose the table
        selection_table_name = st.selectbox(
            label="請選擇資料表", placeholder="", options=option.table_options.keys()
        )
        if selection_table_name is not None:
            table_id = option.table_options[selection_table_name]

    with col2:
        # choose the sport
        sport = st.selectbox(
            label="請選擇運動", placeholder="", options=option.sport_options
        )
        if sport is None:
            sport = "NBA"

    with col3:
        # choose the rank time
        rank_time = st.selectbox(
            label="請選擇排行榜時間", placeholder="", options=option.ranktime_options
        )
        if rank_time is None:
            rank_time = "lastmonth"

    with col4:
        # choose the rank time: eg. 3 show the 3 most popular predicitons
        rank = st.number_input(
            label="請選擇預測數量", placeholder="", min_value=1, max_value=5, value=1
        )

    # choose the date range
    selection_date = st.date_input(
        label="請選擇日期",
        value=(option.today, option.today),
        min_value=dt.date(2024, 1, 3),
        max_value=option.today,
    )
    if isinstance(selection_date, tuple) and len(selection_date) == 2:
        start_date, end_date = str(selection_date[0]), str(selection_date[1])
    else:
        st.warning("選擇日期有誤，請重新選擇")

    submit_button = st.form_submit_button(label="開始搜尋")


if submit_button:
    with st.spinner("請耐心等候資料擷取..."):
        # filter the dataframe according to the input options
        filterdf = helper.filter_dataframe(
            rawdf, sport, rank_time, rank, start_date, end_date
        )

        # summarize the result
        sumdf = helper.summeraize_outcome(filterdf)
        fig = helper.pie_outcome(sumdf)
        st.plotly_chart(fig, use_container_width=True)
        st.table(filterdf)
