import time
import requests
import os
from influxdb import InfluxDBClient

DATABASE = "rates"
RATES_URL = "https://api.transferwise.com/v1/rates?source=CHF"
RATES_INTERVAL = 12


def setup(client):
    client.create_database(DATABASE)
    client.create_retention_policy("hp", "14d", 1, database=DATABASE, default=True)


def write_rates_forever(client):

    while True:
        headers = {"Authorization": "Bearer {}".format(os.environ["API_TOKEN"])}
        response = requests.get(RATES_URL, headers=headers)
        rates = response.json()

        json_body = [
            {
                "measurement": "CHF",
                "fields": {rate["target"]: rate["rate"] for rate in rates},
            }
        ]

        client.write_points(json_body)
        time.sleep(RATES_INTERVAL)


if __name__ == "__main__":
    client = InfluxDBClient(
        os.environ["INFLUXDB_URL"],
        os.environ["INFLUXDB_PORT"],
        "root",
        "root",
        DATABASE,
    )
    setup(client)
    write_rates_forever(client)
