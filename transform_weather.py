import sys
import logging
from typing import List, Dict, Any
import pandas as pd

# Import the extraction module from get_data.py
from get_data import fetch_raw_weather_data, CITY_LIST, API_KEY

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("WeatherETLPipeline.Transform")


def standardize_raw_payloads(raw_data: List[Dict[str, Any]]) -> pd.DataFrame:
    """Standardizes nested JSON API responses into a clean, typed Pandas DataFrame."""
    logger.info("Standardizing raw JSON payloads into uniform schema...")
    standardized_records = []

    for item in raw_data:
        try:
            record = {
                "city_name": str(item.get("name", "")).strip().title(),
                "temperature_celsius": round(float(item["main"]["temp"]) - 273.15, 2),
                "humidity_pct": int(item["main"]["humidity"]),
                "wind_speed_m_s": float(item["wind"]["speed"]),
                "observation_timestamp": pd.to_datetime(item.get("dt"), unit="s", utc=True),
            }
            standardized_records.append(record)
        except (KeyError, TypeError, ValueError) as err:
            logger.error(f"Failed to standardize raw record {item}: {str(err)}")

    df = pd.DataFrame(standardized_records)
    logger.info(f"Standardized DataFrame constructed with shape: {df.shape}")
    return df


def validate_data_quality(df: pd.DataFrame) -> bool:
    """Executes automated data quality assertions on the standardized DataFrame."""
    if df.empty:
        logger.error("Data Quality check aborted: Input DataFrame is empty.")
        return False

    logger.info("Running Data Quality validation suite...")

    try:
        # Rule 1: Schema & Exact Column Order Verification
        expected_columns = [
            "city_name",
            "temperature_celsius",
            "humidity_pct",
            "wind_speed_m_s",
            "observation_timestamp",
        ]
        assert list(df.columns) == expected_columns, f"Column mismatch. Expected {expected_columns}, got {list(df.columns)}"

        # Rule 2: Null Value Assertions
        assert df["city_name"].notnull().all(), "Null values found in city_name"
        assert df["temperature_celsius"].notnull().all(), "Null values found in temperature_celsius"
        assert df["observation_timestamp"].notnull().all(), "Null values found in observation_timestamp"

        # Rule 3: Business Domain Range Validations
        assert df["temperature_celsius"].between(-60.0, 60.0).all(), "Temperature value out of bounds (-60 to 60 C)"
        assert df["humidity_pct"].between(0, 100).all(), "Humidity value out of bounds (0 to 100%)"
        assert df["wind_speed_m_s"].between(0.0, 150.0).all(), "Wind speed value out of bounds (0 to 150 m/s)"

        # Rule 4: Allowed Values Set Check
        allowed_cities = {"London", "Paris", "Tokyo"}
        assert set(df["city_name"]).issubset(allowed_cities), "Unexpected city found in dataset"

        logger.info("SUCCESS: All Data Quality assertions PASSED.")
        return True

    except AssertionError as err:
        logger.error(f"FAILURE: Data Quality validation gate failed! Reason: {str(err)}")
        return False


def get_clean_weather_data() -> pd.DataFrame:
    """Orchestrates Extraction, Transformation, and Quality Validation.
    Returns the cleansed DataFrame for downstream modules like load.py."""
    logger.info("Fetching and preparing weather data...")

    # Step 1: Extract
    all_weather_data = fetch_raw_weather_data(CITY_LIST, API_KEY)
    if not all_weather_data:
        logger.critical("No data retrieved from API.")
        raise ValueError("API Extraction returned an empty dataset.")

    # Step 2: Standardize
    standardized_df = standardize_raw_payloads(all_weather_data)

    # Step 3: Validate
    quality_passed = validate_data_quality(standardized_df)
    if not quality_passed:
        logger.critical("Data Quality gate failed!")
        raise ValueError("Data Quality assertions failed.")

    return standardized_df


def load_to_silver_layer(clean_df: pd.DataFrame) -> None:
    """Simulates persisting validated, standardized data into Silver storage layer."""
    logger.info("Persisting validated records to Silver storage layer...")

    print("\n" + "=" * 80)
    print("CLEANSED & VALIDATED SILVER DATASET")
    print("=" * 80)
    print(clean_df.to_string(index=False))
    print("=" * 80 + "\n")

    logger.info("Pipeline execution complete. Silver layer successfully loaded.")


def run_etl_pipeline():
    """Orchestrates Extraction, Standardization, Quality Validation, and Loading."""
    logger.info("Starting Weather ETL Pipeline execution...")
    clean_df = get_clean_weather_data()
    load_to_silver_layer(clean_df)


if __name__ == "__main__":
    run_etl_pipeline()