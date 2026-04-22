import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import pandas as pd
import logging
from configs.config import RAW_PATH, PROCESSED_PATH

# ---------------- LOGGING SETUP ---------------- #
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ---------------- LOAD DATA ---------------- #
def load_data(path):
    logging.info("Loading raw data...")
    df = pd.read_json(path, lines=True)
    return df


# ---------------- CLEAN DATA ---------------- #
def clean_data(df):
    logging.info("Cleaning data...")

    # Validation checks
    if df.empty:
        raise ValueError("Input data is empty!")

    required_cols = ["symbol", "price", "timestamp"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    # Convert timestamp
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Remove invalid prices
    df = df[df["price"] > 0]

    # Remove missing values
    df = df.dropna()

    return df


# ---------------- FEATURE ENGINEERING ---------------- #
def feature_engineering(df):
    logging.info("Performing feature engineering...")

    # Extract date features
    df["date"] = df["timestamp"].dt.date
    df["hour"] = df["timestamp"].dt.hour

    # Sort before calculating diff
    df = df.sort_values(["symbol", "timestamp"])

    # Price change per stock
    df["price_change"] = df.groupby("symbol")["price"].diff()

    # Rolling average price
    df["rolling_price"] = df.groupby("symbol")["price"].transform(
        lambda x: x.rolling(window=5).mean()
    )

    # Volume spike detection
    df["volume_spike"] = df["volume"] > df["volume"].mean()

    return df


def save_data(df, path):
    logging.info("Saving processed data...")

    # Create directory if not exists
    os.makedirs(os.path.dirname(path), exist_ok=True)

    df.to_csv(path, index=False)


# ---------------- MAIN PIPELINE ---------------- #
def run_etl():
    try:
        df = load_data(RAW_PATH)
        df = clean_data(df)
        df = feature_engineering(df)
        save_data(df, PROCESSED_PATH)

        logging.info("✅ ETL pipeline completed successfully!")

    except Exception as e:
        logging.error(f"❌ ETL failed: {e}")


# ---------------- ENTRY POINT ---------------- #
if __name__ == "__main__":
    run_etl()