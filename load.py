import pandas as pd
from sqlalchemy import create_engine
from transform_weather import get_clean_weather_data
# 1. Fetch the cleansed DataFrame from transform_weather
standardized_df = get_clean_weather_data()
# 1. Define your PostgreSQL credentials
DB_USER = "postgres"
DB_PASS = "user"
DB_HOST = "localhost"  # or your database host IP
DB_PORT = "5432"  # default Postgres port
DB_NAME = "weather_db"

# 2. Build the SQLAlchemy Connection URI String
# Format: postgresql+psycopg2://user:password@host:port/dbname
db_uri = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 3. Create the SQLAlchemy Engine
engine = create_engine(db_uri)

# 4. Load your DataFrame into PostgreSQL
standardized_df.to_sql(
    name="weather_reports",  # Target table name in Postgres
    con=engine,  # Pass the SQLAlchemy Engine
    if_exists="append",  # Options: 'append' (add rows), 'replace' (drop & recreate), 'fail'
    index=False,  # Don't save the DataFrame index as a column
)

print(f"Data successfully loaded into PostgreSQL database '{DB_NAME}'")