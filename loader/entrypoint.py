import time
import os
from influxdb_client import InfluxDBClient

url = os.getenv("INFLUX_URL", "http://influxdb:8086")
username = os.getenv("INFLUX_USERNAME", "admin")
password = os.getenv("INFLUX_PASSWORD", "adminpassword")
org = os.getenv("INFLUX_ORG", "example-org")

def wait_for_influx(timeout=60, interval=2):
    client = InfluxDBClient(url=url, username=username, password=password, org=org)
    waited = 0
    while waited < timeout:
        try:
            health = client.health()
            if getattr(health, "status", None) == "pass":
                print("InfluxDB is healthy")
                return True
            else:
                print(f"InfluxDB health: {getattr(health,'status', None)} - waiting...")
        except Exception as e:
            print(f"Waiting for InfluxDB ({e})")
        time.sleep(interval)
        waited += interval
    return False

if __name__ == "__main__":
    if wait_for_influx(timeout=120, interval=2):
        # run the loader script (assumes load_sample_data.py is in the image)
        import load_sample_data
        load_sample_data.load_data()
    else:
        print("Timed out waiting for InfluxDB to become healthy")
        raise SystemExit(1)
