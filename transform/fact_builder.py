import numpy as np
import pandas as pd

def build_fact_sessions(session_df, dim_channel_df, dim_status_df, dim_date_df, dim_user_df):
    fact = session_df.copy()
    fact = fact.merge(dim_channel_df, on="channel_code", how="left")
    fact = fact.merge(dim_status_df, on="status_code", how="left")

    registered_ids = set(dim_user_df["user_id"])
    fact["is_registered"] = fact["user_id"].isin(registered_ids)
    fact["user_id"] = np.where(fact["is_registered"], fact["user_id"], -1)

    fact["start_date"] = pd.to_datetime(fact["start_datetime"], errors="coerce")
    fact["end_date"] = pd.to_datetime(fact["end_datetime"], errors="coerce")
    fact["duration_minutes"] = (fact["end_date"] - fact["start_date"]).dt.total_seconds() / 60

    fact = fact.merge(dim_date_df[["date", "date_id"]],
                      left_on="start_date", right_on="date", how="left")

    return fact[[
        "play_session_id", "user_id", "channel_id", "status_id", "date_id",
        "total_score", "duration_minutes", "is_registered"
    ]]

def build_fact_user_plan(user_plan_df, dim_date_df, dim_plan_df):
    df = user_plan_df.copy()

    df["end_date"] = df["end_date"].replace(
        to_replace=r"^9999\-01\-01.*", value=pd.NaT, regex=True
    )
    df["start_date"] = pd.to_datetime(df["start_date"], errors="coerce")
    df["end_date"] = pd.to_datetime(df["end_date"], errors="coerce")

    df = df.merge(dim_date_df[["date", "date_id"]],
                  left_on="start_date", right_on="date", how="left") \
           .rename(columns={"date_id": "start_date_id"}).drop(columns="date")

    df = df.merge(dim_date_df[["date", "date_id"]],
                  left_on="end_date", right_on="date", how="left") \
           .rename(columns={"date_id": "end_date_id"}).drop(columns="date")

    df = df.merge(dim_plan_df[["plan_id", "payment_frequency_code", "cost_amount"]],
                  on="plan_id", how="left")

    return df[[
        "user_registration_id", "payment_detail_id", "plan_id",
        "start_date_id", "end_date_id", "payment_frequency_code", "cost_amount"
    ]]

