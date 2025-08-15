import pytest
import pandas as pd

from extract.extract import extract_all
from transform.dim_builder import (
    build_dim_user, build_dim_plan, build_dim_payment, build_dim_channel, build_dim_status, build_dim_date
)
from transform.fact_builder import build_fact_sessions, build_fact_user_plan
from analysis.insights import *

@pytest.fixture(scope="module")
def data():
    dfs = extract_all()

    dim_user = build_dim_user(dfs["user"], dfs["user_registration"])
    dim_plan = build_dim_plan(dfs["plan"], dfs["plan_freq"])
    dim_payment = build_dim_payment(dfs["user_payment"])
    dim_channel = build_dim_channel(dfs["channel"])
    dim_status = build_dim_status(dfs["status"])
    dim_date = build_dim_date(dfs["user_plan"], dfs["sessions"])

    fact_sessions = build_fact_sessions(dfs["sessions"], dim_channel, dim_status, dim_date, dim_user)
    fact_user_plan = build_fact_user_plan(dfs["user_plan"], dim_date, dim_plan)

    return {
        "dim_user": dim_user,
        "dim_plan": dim_plan,
        "dim_payment": dim_payment,
        "dim_channel": dim_channel,
        "dim_status": dim_status,
        "dim_date": dim_date,
        "fact_sessions": fact_sessions,
        "fact_user_plan": fact_user_plan
    }

def test_dim_user_integrity(data):
    dim_user = data["dim_user"]
    assert not dim_user["user_registration_id"].isnull().all()  
    assert (dim_user["user_id"] == -1).any() 
    assert dim_user["user_registration_id"].nunique() <= len(dim_user)

def test_dim_plan_columns(data):
    dim_plan = data["dim_plan"]
    expected_columns = {"plan_id", "payment_frequency_code", "cost_amount", "english_description"}
    assert expected_columns.issubset(set(dim_plan.columns))

def test_fact_sessions_columns(data):
    fact_sessions = data["fact_sessions"]
    expected_cols = {
        "play_session_id", "user_id", "channel_id",
        "status_id", "date_id", "total_score", "duration_minutes", "is_registered"
    }
    assert expected_cols.issubset(set(fact_sessions.columns))
    assert fact_sessions["play_session_id"].is_unique

def test_fact_user_plan_columns(data):
    fact_user_plan = data["fact_user_plan"]
    expected_cols = [
        "user_registration_id", "payment_detail_id", "plan_id",
        "start_date_id", "end_date_id", "payment_frequency_code", "cost_amount"
    ]
    assert set(expected_cols).issubset(set(fact_user_plan.columns))

def test_payment_frequency_code_present(data):
    fact_user_plan = data["fact_user_plan"]
    assert fact_user_plan["payment_frequency_code"].notnull().all()

def test_registered_vs_unregistered_flags(data):
    fact_sessions = data["fact_sessions"]
    assert fact_sessions["is_registered"].dtype == bool
    assert fact_sessions["is_registered"].any() and (~fact_sessions["is_registered"]).any()

def test_no_null_critical_columns(data):
    fact_sessions = data["fact_sessions"]
    fact_user_plan = data["fact_user_plan"]

    critical_cols_sessions = ["user_id", "channel_id", "status_id", "play_session_id"]
    for col in critical_cols_sessions:
        assert not fact_sessions[col].isnull().any()

    critical_cols_user_plan = ["user_registration_id", "plan_id", "start_date_id"]
    for col in critical_cols_user_plan:
        if col != "user_registration_id":
            assert not fact_user_plan[col].isnull().any()

def test_unique_keys_in_dimensions(data):
    assert data["dim_user"]["user_id"].is_unique
    assert data["dim_plan"]["plan_id"].is_unique
    assert data["dim_channel"]["channel_id"].is_unique
    assert data["dim_status"]["status_id"].is_unique

def test_no_orphan_users_in_fact_sessions(data):
    fact_sessions = data["fact_sessions"]
    dim_user = data["dim_user"]
    orphan_ids = set(fact_sessions["user_id"]) - set(dim_user["user_id"])
    assert len(orphan_ids) == 0

def test_gross_revenue_positive(data):
    fact_user_plan = data["fact_user_plan"]
    revenue = gross_revenue(fact_user_plan)
    assert revenue >= 0

def test_session_counts_platform(data):
    fact_sessions = data["fact_sessions"]
    dim_channel = data["dim_channel"]
    counts = session_count_by_platform(fact_sessions, dim_channel)
    assert (counts >= 0).all()

