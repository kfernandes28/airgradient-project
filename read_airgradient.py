import requests 
from datetime import datetime
import csv
import os

url = "http://192.168.0.140/measures/current"

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

reading = {
    "timestamp": timestamp,
    "temperature_c": temperature,
    "co2_ppm": co2,
    "pm25_ugm3": pm25,
    "humidity_pct": humidity,
    "voc_index": voc,
    "nox_index": nox,
}

print (reading)

file_exists = os.path.exists("airgradient_readings.csv")

with open("airgradient_readings.csv", "a", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=reading.keys())

    if not file_exists:
        writer.writeheader()

    writer.writerow(reading)