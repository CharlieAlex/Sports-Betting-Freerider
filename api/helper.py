import pandas as pd
import plotly.express as px
from plotly.graph_objs import Figure
import datetime as dt

all_3months_query = """
    WITH date_range AS (
        SELECT
            CURRENT_DATE() AS end_date,
            DATE_TRUNC(DATE_SUB(CURRENT_DATE(), INTERVAL 3 MONTH), MONTH) AS start_date
    )
    SELECT DISTINCT
        date, game, prediction, during, sport, rank, outcome
    FROM 
        `sport-lottery-database.playsports.total_result`
    WHERE 
        date >= (SELECT start_date FROM date_range)
        AND date <= (SELECT end_date FROM date_range)
    UNION ALL
    SELECT DISTINCT
        date, game, prediction, during, sport, rank, outcome
    FROM 
        `sport-lottery-database.playsports.mainpush_result`
    WHERE 
        date >= (SELECT start_date FROM date_range)
        AND date <= (SELECT end_date FROM date_range)
"""


def make_query(
    table_id: str,
    sport: str,
    rank_time: str,
    rank: float,
    start_date: str,
    end_date: str,
) -> str:
    query = f"""
        SELECT DISTINCT
            date, game, prediction, rank, outcome
        FROM 
            `sport-lottery-database.playsports.{table_id}`
        WHERE 
            date >= "{start_date}"
            AND date <= "{end_date}"
            AND sport = "{sport}"
            AND during = "{rank_time}"
            AND rank <= {rank}
        ORDER BY
            date DESC, game, prediction, rank
    """
    return query


def true_ratio(df: pd.DataFrame, start_date: dt.date, end_date: dt.date) -> float:
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    result = (
        df.query(f"date >= '{start_date_str}' and date <= '{end_date_str}'")["outcome"]
        .value_counts(normalize=True)
        .get("準")
    )
    proportion = result if result is not None else 0
    return round(proportion * 100, 2)


def pred_count(df: pd.DataFrame, start_date: dt.date, end_date: dt.date) -> int:
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    result = df.query(
        f"date >= '{start_date_str}' and date <= '{end_date_str}'"
    ).count()["prediction"]
    return int(result)


def na_count(df: pd.DataFrame, start_date: dt.date, end_date: dt.date) -> int:
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    filtered_df = df.query(f"date >= '{start_date_str}' and date <= '{end_date_str}'")
    return filtered_df[~filtered_df["outcome"].isin(["準", "囧"])].shape[0]


def hist_overall_outcome(df: pd.DataFrame, rank_time: str) -> Figure:
    df_ratio = (
        df.query(f"during == '{rank_time}'")
        .groupby(["sport", "during", "outcome"])
        .size()
        .reset_index()
        .rename(columns={0: "count"})
    )

    fig = px.bar(
        df_ratio,
        y="sport",
        x="count",
        color="outcome",
        barmode="group",
        title=f"整體預測表現-{rank_time}",
        labels={"count": "數量", "sport": "運動", "during": "排行榜時間"},
        orientation="h",
    )
    fig.update_xaxes(title_text="運動")
    fig.update_yaxes(title_text=None)

    return fig


def filter_dataframe(
    df: pd.DataFrame,
    sport: str,
    rank_time: str,
    rank: float,
    start_date: str,
    end_date: str,
) -> pd.DataFrame:
    df["date"] = pd.to_datetime(df["date"])

    filtered_df = df[
        (df["date"] >= pd.to_datetime(start_date))
        & (df["date"] <= pd.to_datetime(end_date))
        & (df["sport"] == sport)
        & (df["during"] == rank_time)
        & (df["rank"] <= rank)
    ]
    filtered_df = (
        filtered_df.drop(
            columns=["sport", "during"],
        )
        .drop_duplicates(
            subset=["date", "game", "prediction", "rank", "outcome"],
        )
        .sort_values(
            by=["date", "game", "prediction", "rank"],
            ascending=[False, True, True, True],
        )
    )

    return filtered_df


def summeraize_outcome(df: pd.DataFrame) -> pd.DataFrame:
    df_ratio = (
        df.outcome.value_counts(normalize=True, dropna=False)
        .reset_index()
        .sort_values("outcome")
    )

    df_count = (
        df.outcome.value_counts(dropna=False)
        .reset_index()
        .sort_values("outcome")["count"]
    )
    return pd.concat([df_ratio, df_count], axis=1)


def pie_outcome(df: pd.DataFrame) -> Figure:
    fig = px.pie(
        df,
        values="proportion",
        names="outcome",
        title="Proportion of Outcomes",
        hover_data={"count": True},
    )
    return fig
