from config.settings import OUTPUT_DIR

def save_df(df, filename):
    df.to_csv(OUTPUT_DIR / filename, index=False)
