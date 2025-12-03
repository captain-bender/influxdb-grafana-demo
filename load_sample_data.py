"""
Load sample air sensor data into InfluxDB programmatically
Run this script after starting the InfluxDB container
"""
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime, timedelta, timezone
import random
import os

# InfluxDB connection details - allow overrides from environment when running in Docker
url = os.getenv("INFLUX_URL", "http://localhost:8086")
username = os.getenv("INFLUX_USERNAME", "admin")
password = os.getenv("INFLUX_PASSWORD", "adminpassword")
org = os.getenv("INFLUX_ORG", "example-org")
bucket = os.getenv("INFLUX_BUCKET", "example-bucket")

def generate_sample_data(hours=48):
    """Generate sample air sensor data for the specified number of hours"""
    sensors = ["TLM0100", "TLM0101", "TLM0102", "TLM0103"]
    locations = ["Warehouse-1", "Warehouse-2", "Office-1", "Office-2"]
    
    data_points = []
    start_time = datetime.now(timezone.utc) - timedelta(hours=hours)
    
    # Generate data points every 5 minutes
    for i in range(int(hours * 12)):  # 12 points per hour (every 5 min)
        timestamp = start_time + timedelta(minutes=i * 5)
        
        for sensor_id, location in zip(sensors, locations):
            # Generate realistic sensor readings with some variation
            base_temp = 20 + random.uniform(-2, 2)
            base_humidity = 40 + random.uniform(-5, 5)
            base_co = 0.5 + random.uniform(-0.1, 0.1)
            
            data_points.append({
                "measurement": "airSensors",
                "tags": {
                    "sensor_id": sensor_id,
                    "location": location
                },
                "fields": {
                    "temperature": round(base_temp + random.uniform(-1, 1), 2),
                    "humidity": round(base_humidity + random.uniform(-3, 3), 2),
                    "co": round(base_co + random.uniform(-0.05, 0.05), 3)
                },
                "time": timestamp
            })
    
    return data_points

def load_data():
    """Connect to InfluxDB and load sample data"""
    print(f"Connecting to InfluxDB at {url}...")
    
    try:
        # Create client using username/password
        client = InfluxDBClient(url=url, username=username, password=password, org=org)
        
        # Test connection
        health = client.health()
        if health.status != "pass":
            print(f"InfluxDB is not healthy: {health.message}")
            return
        
        print("Connected successfully!")
        
        # Generate sample data
        print("Generating sample data...")
        data_points = generate_sample_data(hours=48)
        print(f"Generated {len(data_points)} data points")
        
        # Write data
        print(f"Writing data to bucket '{bucket}'...")
        write_api = client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket=bucket, org=org, record=data_points)
        
        print("Sample data loaded successfully!")
        print(f"  - {len(data_points)} data points written")
        print(f"  - Time range: last 48 hours")
        print(f"  - Sensors: TLM0100, TLM0101, TLM0102, TLM0103")
        print(f"  - Fields: temperature, humidity, co")
        
        client.close()
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure:")
        print("1. InfluxDB is running (docker compose up -d)")
        print("2. The container has fully initialized (wait 10-15 seconds after starting)")
        print("3. You've installed the required package: pip install influxdb-client")
        print("4. Credentials are correct (username: admin, password: adminpassword)")

if __name__ == "__main__":
    load_data()
