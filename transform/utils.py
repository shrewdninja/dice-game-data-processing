import pandas as pd

def build_date_dim(dates):
    """Create date dimension from multiple date columns."""
    s = pd.Series(pd.to_datetime(dates).dropna().unique())
    dim_date = pd.DataFrame({"date": s})
    dim_date["date_id"] = dim_date["date"].rank(method="dense").astype(int)
    dim_date["year"] = dim_date["date"].dt.year
    dim_date["month"] = dim_date["date"].dt.month
    dim_date["day"] = dim_date["date"].dt.day
    return dim_date.sort_values("date_id")
