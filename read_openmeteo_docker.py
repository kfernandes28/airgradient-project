import requests
from datetime import datetime, timezone
import math
import psycopg
import os
import time

url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": 51.5209,
	"longitude": -0.672,
	"current": ["temperature_2m", "relative_humidity_2m"],
	"timezone": "Europe/London",
    "timeformat": "unixtime",
}

def calculate_dew_point(temperature_c, humidity_pct):
    a = 17.62
    b = 243.12

    gamma = (
        math.log(humidity_pct / 100.0)
        + (a * temperature_c) / (b + temperature_c)
    )

    return round((b * gamma) / (a - gamma),2)

while True:
    try:

        response = requests.get(url, params = params, timeout=10)

        response.raise_for_status()

        data = response.json()

        temperature = data["current"]["temperature_2m"]
        humidity = data["current"]["relative_humidity_2m"]
        estimated_at = datetime.fromtimestamp(data["current"]["time"], tz=timezone.utc)
        retrieved_at = datetime.now(timezone.utc)

        dew_point = calculate_dew_point(temperature,humidity)

        reading = {
            "estimated_at": estimated_at,
            "retrieved_at": retrieved_at,
            "temperature_c": temperature,
            "humidity_pct": humidity,
            "dew_point_c": dew_point,
        }

        print (reading)

        with psycopg.connect(
            host=os.environ["POSTGRES_HOST"],
            port=os.environ["POSTGRES_PORT"],
            dbname=os.environ["POSTGRES_DB"],
            user=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"]
        ) as connection:

            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO openmeteo_readings (
                        estimated_at,
                        retrieved_at,
                        temperature_c,
                        humidity_pct,
                        dew_point_c
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (estimated_at) DO NOTHING
                    """,
                    (
                        reading["estimated_at"],
                        reading["retrieved_at"],
                        reading["temperature_c"],
                        reading["humidity_pct"],
                        reading["dew_point_c"],
                    )
                )
        #with psycopg.connect(...) as connection: opens the connection, commits on success or rolls back on failure, then closes it.
        #with connection.cursor() as cursor: creates the cursor and closes it automatically.

    except (requests.RequestException, psycopg.Error) as e:
        print(f"Collection failed: {e}")

    time.sleep(900)