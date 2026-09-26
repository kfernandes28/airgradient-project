import requests 
from datetime import datetime

import math
import psycopg
import time
import os

url = "http://192.168.0.140/measures/current"

def calculate_dew_point(temperature_c, humidity_pct):
    a = 17.62
    b = 243.12

    gamma = (
        math.log(humidity_pct / 100.0)
        + (a * temperature_c) / (b + temperature_c)
    )

    return round((b * gamma) / (a - gamma),2)


while True:
    # get + store one reading
    response =requests.get(url)

    data = response.json()

    #print (data)

    temperature = data["atmp"]
    co2 = data["rco2"]
    pm25 = data["pm02"]
    humidity = data["rhum"]
    voc = data["tvocIndex"]
    nox = data["noxIndex"]
    timestamp = datetime.now().isoformat()

    dew_point = calculate_dew_point(temperature, humidity)

    reading = {
        "timestamp": timestamp,
        "temperature_c": temperature,
        "co2_ppm": co2,
        "pm25_ugm3": pm25,
        "humidity_pct": humidity,
        "dew_point_c": dew_point,
        "voc_index": voc,
        "nox_index": nox,
    }

    print (reading)

    connection = psycopg.connect(
        host=os.environ["POSTGRES_HOST"],
        port=os.environ["POSTGRES_PORT"],
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"]
    )

    cursor = connection.cursor()


    cursor.execute(
        """
        INSERT INTO airgradient_readings (
            timestamp,
            temperature_c,
            co2_ppm,
            pm25_ugm3,
            humidity_pct,
            dew_point_c,
            voc_index,
            nox_index
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            reading["timestamp"],
            reading["temperature_c"],
            reading["co2_ppm"],
            reading["pm25_ugm3"],
            reading["humidity_pct"],
            reading["dew_point_c"],
            reading["voc_index"],
            reading["nox_index"],
        )
    )

    connection.commit() #make it permanent
    cursor.close()
    connection.close()

    #we currently open a PostgreSQL connection, insert one reading, commit, then close the connection inside every loop iteration,

    time.sleep(120)