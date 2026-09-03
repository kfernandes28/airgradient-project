# AirGradient Air Quality Monitoring Project

## Why I built this

I originally bought an AirGradient monitor because I wanted more visibility into the air I was breathing at home from a health perspective.

AirGradient already provides its own dashboard, but I wanted more control over how my data was stored and visualised long term. I had also seen people integrate AirGradient devices with tools such as Home Assistant, which made me curious about building my own local monitoring pipeline.

Around the same time, AirGradient announced plans to introduce subscription fees for some more demanding dashboard features, including longer-term historical data storage. I appreciated their transparency around the infrastructure costs involved, but it gave me an extra push to stop delaying and explore storing the data myself.

Grafana and observability were also topics I was increasingly encountering at work, so this project felt like a good opportunity to learn those concepts properly by applying them to something I already cared about.

The result is a small self-hosted monitoring stack that:

- collects readings directly from an AirGradient device over the local network
- stores the readings in PostgreSQL
- visualises the data in Grafana
- runs the collector, database and Grafana as Docker containers managed with Docker Compose

## Architecture

```text
AirGradient sensor
        ↓
Python collector
        ↓
PostgreSQL
        ↓
Grafana
```

The Python collector requests the AirGradient `/measures/current` endpoint every two minutes and stores temperature, CO₂, PM2.5, humidity, VOC index and NOx index readings in PostgreSQL. Grafana connects to PostgreSQL over the internal Docker network and is exposed on port 3000 for browser access.

## Project evolution

The project was built incrementally:

1. **CSV prototype** – fetched readings from the AirGradient API and stored them locally in CSV.
2. **PostgreSQL version** – replaced CSV storage with a PostgreSQL database running locally on my Mac.
3. **Dockerised collector** – moved the collector and database into Docker containers on a Windows machine intended to run the monitoring stack more continuously.
4. **Docker Compose stack** – brought PostgreSQL, the collector and Grafana together into one reproducible stack.

Earlier versions of the collector are kept in the `archive/` directory to show this progression.

## Technologies

- Python
- PostgreSQL
- Docker
- Docker Compose
- Grafana
- AirGradient local API

## What I learned

What started as a simple attempt to store my own air-quality data ended up taking me down a much broader learning path through networking, APIs, databases, Docker and observability.

This project gave me practical experience with:

- Docker images and containers
- persistent Docker volumes
- container networking and DNS
- host vs container ports
- environment variables for configuration and credentials
- Docker Compose for managing multiple services
- storing time-series sensor data in PostgreSQL
- connecting Grafana to a PostgreSQL data source
- building a simple always-running data collection pipeline