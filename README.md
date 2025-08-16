# Dice Game Comprehensive Data Analytics Application

This project is created for processing and analyzing data from a dice game application, designed to provide key analytics on user activities, payments, and sessions. It supports both registered and unregistered players and offers detailed insights by platform and payment behavior.

## Overview
- **Objective**: Derive key insights from given data to predict the growth for 2025.
- **Technologies**: Python

## Key Features
- Robust handling of unregistered (guest) players with a dedicated user record.
- Date field normalization with invalid or open-ended dates standardized.
- Referential integrity ensured between fact tables and dimension tables.
- Comprehensive analytical insights for session counts, revenue, payment types, completion rates, registered vs. unregistered user activity by platform, and more.
- Extensive automated testing suite verifying data integrity, uniqueness, validity, and business logic.
- Modular design allowing for easy maintenance and extension.

## Setup
git clone <repository-url>
cd dice-game-data-processing

pip install -r requirements.txt
- **This will print out key analytics:**
python main.py
- **This will run automated pytests:**
pytest tests/test_etl_pipeline_pytest.py

