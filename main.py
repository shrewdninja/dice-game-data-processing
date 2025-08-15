from extract.extract import extract_all
from transform.dim_builder import *
from transform.fact_builder import *
from load.load import save_df
from analysis.insights import *

def main():
    dfs = extract_all()
    dim_user = build_dim_user(dfs["user"], dfs["user_registration"])
    dim_plan = build_dim_plan(dfs["plan"], dfs["plan_freq"])
    dim_payment = build_dim_payment(dfs["user_payment"])
    dim_channel = build_dim_channel(dfs["channel"])
    dim_status = build_dim_status(dfs["status"])
    dim_date = build_dim_date(dfs["user_plan"], dfs["sessions"])

    fact_sessions = build_fact_sessions(dfs["sessions"], dim_channel, dim_status, dim_date, dim_user)
    fact_user_plan = build_fact_user_plan(dfs["user_plan"], dim_date, dim_plan)

    save_df(dim_user, "dim_user.csv")
    save_df(dim_plan, "dim_plan.csv")
    save_df(dim_payment, "dim_payment_method.csv")
    save_df(dim_channel, "dim_channel.csv")
    save_df(dim_status, "dim_status.csv")
    save_df(dim_date, "dim_date.csv")
    save_df(fact_sessions, "fact_play_sessions.csv")
    save_df(fact_user_plan, "fact_user_plan.csv")

    print("\n--- Insights ---")
    print("Sessions by Channel:\n", sessions_by_channel(fact_sessions, dim_channel))
    print("\nRevenue by Frequency:\n", revenue_by_frequency(fact_user_plan, dim_plan))
    print("\nCompletion Rate:\n", completion_rate(fact_sessions, dim_status, dim_channel))
    print("\nSessions by Registration Status and Platform:\n",
          platform_sessions_by_registration(fact_sessions, dim_channel))
    print("\nPercent Registered by Platform:\n",
          percent_registered_by_platform(fact_sessions, dim_channel))
    print("\nSession Count by Platform (Browser vs Mobile App):\n",
          session_count_by_platform(fact_sessions, dim_channel))
    print("\nUser Count by Payment Frequency:\n", user_count_by_payment_frequency(fact_user_plan))
    print("\nGross Revenue from the App:\n",
          gross_revenue(fact_user_plan))


if __name__ == "__main__":
    main()
