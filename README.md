Weather ETL Pipeline

A lightweight Python ETL pipeline that collects real-time weather data from the OpenWeatherMap API for multiple cities around the world.

The project is designed as a simple starting point for building a larger data pipeline, with separate steps for extracting, transforming, and eventually loading weather data into a database or cloud storage system.

  Features
Real-time weather extraction
Fetches current weather information for multiple cities using the OpenWeatherMap API.
Multiple city support
Easily collect weather data for cities such as London, Paris, Tokyo, New York, Cairo, and more.
Error handling
Handles common API and network errors, including HTTP errors and request timeouts.
Logging
Uses Python logging to keep track of pipeline activity and make troubleshooting easier.
Modular structure
The extraction logic is organized into reusable Python functions, making it easy to add transformation and loading steps later.
📁 Project Structure
weather-etl/
│
├── get_data.py      # Fetches raw weather data from OpenWeatherMap
├── get-pip.py       # Optional script for bootstrapping pip
└── README.md        # Project documentation
🚀 Getting Started
Prerequisites

Make sure you have:

Python 3.9 or newer
An OpenWeatherMap API key
Internet access

Python 3.9–3.12 is recommended.

1. Clone the Repository
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
2. Make Sure pip Is Installed

Most Python installations already include pip.

If yours doesn't, you can use the included bootstrap script:

python get-pip.py
3. Install Dependencies

Install the required Python package:

pip install requests
🔑 API Key Setup

You'll need an API key from OpenWeatherMap to use the pipeline.

For security, don't hardcode your API key directly into the source code, especially if you're planning to publish the project on GitHub.

A better approach is to store the key as an environment variable.

For example:

export OPENWEATHER_API_KEY="your-api-key"

On Windows PowerShell:

$env:OPENWEATHER_API_KEY="your-api-key"

Then your Python application can read the key from the environment.

⚙️ Usage

Once your API key and dependencies are configured, run the extraction script:

python get_data.py

You can also import the extraction function into another Python script and provide your own list of cities:

from get_data import fetch_raw_weather_data

cities = ["New York", "Cairo", "Tokyo"]

api_key = "0ef77af5425ce53ed86091e4e0fcb3d0"

weather_data = fetch_raw_weather_data(
    cities=cities,
    api_key=0ef77af5425ce53ed86091e4e0fcb3d0
)

print(weather_data)

This returns the raw weather data collected from OpenWeatherMap, which can then be passed to the transformation and loading stages of the pipeline.

🔄 Pipeline Overview

The project currently focuses on the Extract stage of the ETL process.

OpenWeatherMap API
        │
        ▼
    Extract
        │
        ▼
  Raw Weather Data
        │
        ▼
    Transform
        │
        ▼
 Structured Data
        │
        ▼
      Load
        │
        ▼
Database / Cloud Storage
