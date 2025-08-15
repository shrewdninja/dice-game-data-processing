def sessions_by_channel(fact_sessions, dim_channel):
    df = fact_sessions.merge(dim_channel, on="channel_id")
    return df.groupby("channel_name")["play_session_id"].count()

def revenue_by_frequency(fact_user_plan, dim_plan):
    return fact_user_plan.groupby("payment_frequency_code")["cost_amount"].sum()

def completion_rate(fact_sessions, dim_status, dim_channel):
    completed = fact_sessions.merge(dim_status, on="status_id") \
                              .query("status_code == 'COMPLETED'") \
                              .groupby("channel_id")["play_session_id"].count()
    total = fact_sessions.groupby("channel_id")["play_session_id"].count()
    rate = (completed / total * 100).round(2).fillna(0)
    return rate.rename("completion_rate_%").reset_index() \
               .merge(dim_channel, on="channel_id")

def platform_sessions_by_registration(fact_sessions, dim_channel):
    df = fact_sessions.merge(dim_channel, on="channel_id")
    result = df.groupby(["channel_name", "is_registered"])["play_session_id"] \
               .count().unstack(fill_value=0) \
               .rename(columns={True: "Registered", False: "Unregistered"})
    return result

def percent_registered_by_platform(fact_sessions, dim_channel):
    df = fact_sessions.merge(dim_channel, on="channel_id")
    summary = df.groupby("channel_name")["is_registered"].mean() * 100
    return summary.round(2)

def session_count_by_platform(fact_sessions, dim_channel):
    df = fact_sessions.merge(dim_channel, on="channel_id")
    return df.groupby("channel_name")["play_session_id"].count()

def user_count_by_payment_frequency(fact_user_plan):
    """
    Returns the count of unique registered users grouped by their payment frequency.
    Assumes `payment_frequency_code` and `user_registration_id` columns exist in fact_user_plan.
    """
    registered = fact_user_plan[fact_user_plan["user_registration_id"].notnull()]
    return registered.groupby("payment_frequency_code")["user_registration_id"].nunique()


def gross_revenue(fact_user_plan):
    return fact_user_plan["cost_amount"].sum()
