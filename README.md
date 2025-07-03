# InfluxDB + Grafana Docker Demo

This repository provides a ready-to-use Docker Compose stack for InfluxDB 2.x and Grafana. It is ideal for experimentation, teaching, and building dashboards with time-series data.

## Quick Start
1. Clone the Repository
```
git clone https://github.com/yourusername/influxdb-grafana-demo.git
cd influxdb-grafana-demo
```

2. Start the Stack
```
docker compose up -d
```

3. Access the Services

- **InfluxDB UI:** [http://localhost:8086](http://localhost:8086)
  - Username: `admin`
  - Password: `adminpassword`
  - Organization: `example-org`
  - Bucket: `example-bucket`
  - Admin Token: `admintoken123`
- **Grafana UI:** [http://localhost:3000](http://localhost:3000)
  - Username: `admin`
  - Password: `admin`


## How to Connect Grafana to InfluxDB

1. Log in to Grafana at [http://localhost:3000](http://localhost:3000).
2. Go to **Configuration > Data Sources > Add data source**.
3. Select **InfluxDB**.
4. Set:
   - **URL:** `http://influxdb:8086`
   - **Query Language:** Flux
   - **Organization:** `example-org`
   - **Token:** `admintoken123`
   - **Default Bucket:** `example-bucket`
5. Click **Save & Test**. You should see a success message.


### Load Sample Data

- Use the InfluxDB UI to load the air sensor sample dataset as described in the exercises.


## Visualizing Data in Grafana

After connecting your InfluxDB data source in Grafana:

1. **Create a new Dashboard** and add a new Panel.
2. **In the Query section:**
   - Select your InfluxDB data source.
   - Use the Query Builder or switch to the **Flux** editor.
   - Paste the following sample query (adjust the bucket name if needed):

     ```
     from(bucket: "demo-bucket")
       |> range(start: -30d)
       |> filter(fn: (r) => r._measurement == "airSensors")
       |> filter(fn: (r) => r._field == "temperature")
       |> aggregateWindow(every: 1h, fn: mean)
       |> yield()
     ```
   - You should see a line graph with temperature data if the sample data is loaded.

3. **If you see "No data":**
   - Check and expand the time range in the top right (e.g., "Last 30 days" or "All time").
   - Confirm your bucket and field names match your InfluxDB setup.
   - Try other fields such as `co` or `humidity`.


## Stopping the Stack
```
docker compose down
```

## Notes

- All data is persisted in Docker volumes (`influxdb_data`, `grafana_data`).
- Change default passwords/tokens for production use.

## Troubleshooting

| Issue                  | Solution                                                                                 |
|------------------------|-----------------------------------------------------------------------------------------|
| Grafana shows "No data"| Set a wider time range, check bucket/field names, and use the sample Flux query above.  |
| InfluxDB not loading   | Ensure Docker Desktop is running and ports 8086/3000 are free.                          |
| Container name conflict| Remove existing containers with `docker rm influxdb` or change `container_name`.        |





