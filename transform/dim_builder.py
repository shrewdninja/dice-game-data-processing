import pandas as pd

def build_dim_user(user_df, user_reg_df):
    dim = user_reg_df.merge(user_df, on="user_id", how="left")
    if not (dim["user_id"] == -1).any():
        unreg = pd.DataFrame([{
            "user_registration_id": None,
            "user_id": -1,
            "username": "Unregistered",
            "email": "",
            "first_name": "",
            "last_name": ""
        }])
        dim = pd.concat([dim, unreg], ignore_index=True)
    return dim

def build_dim_plan(plan_df, plan_freq_df):
    return plan_df.merge(plan_freq_df, on="payment_frequency_code", how="left")

def build_dim_payment(user_payment_df):
    return user_payment_df.copy()

def build_dim_channel(channel_df):
    df = channel_df.rename(
        columns={
            "play_session_channel_code": "channel_code",
            "english_description": "channel_name"
        }
    )
    df["channel_id"] = df.index + 1
    return df

def build_dim_status(status_df):
    df = status_df.rename(
        columns={
            "play_session_status_code": "status_code",
            "english_description": "status_name"
        }
    )
    df["status_id"] = df.index + 1
    return df

def build_dim_date(user_plan_df, session_df):
    all_dates = []
    all_dates += list(pd.to_datetime(user_plan_df["start_date"], errors="coerce"))
    all_dates += list(pd.to_datetime(
        user_plan_df["end_date"].replace(r"^9999\-01\-01.*", pd.NaT, regex=True), errors="coerce"))
    all_dates += list(pd.to_datetime(session_df["start_datetime"], errors="coerce"))
    all_dates += list(pd.to_datetime(session_df["end_datetime"], errors="coerce"))
    s = pd.Series(pd.to_datetime(all_dates).dropna().unique())
    dim_date = pd.DataFrame({"date": s})
    dim_date["date_id"] = dim_date["date"].rank(method="dense").astype(int)
    dim_date["year"] = dim_date["date"].dt.year
    dim_date["month"] = dim_date["date"].dt.month
    dim_date["day"] = dim_date["date"].dt.day
    return dim_date.sort_values("date_id")
