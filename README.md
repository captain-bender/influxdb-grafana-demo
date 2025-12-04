# InfluxDB + Grafana Docker Demo

This repository provides a ready-to-use Docker Compose stack for InfluxDB 2.x and Grafana. It is ideal for experimentation, teaching, and building dashboards with time-series data.

## Quick Start
1. Clone the Repository
```
git clone https://github.com/captain-bender/influxdb-grafana-demo
cd influxdb-grafana-demo
```

2. Start the Stack
Make sure that you are inside the project's folder
e.g.
```
cd C:\Users\<your-name>\OneDrive\Documents
cd influx-grafana-demo
```

and then
```
docker compose up -d
```

when your teminal dispays something like "grafana      | logger=infra.usagestats t=2025-12-03T15:32:55.778649174Z level=info msg="Usage stats are ready to report", feel free to continue.

3. Services Details

- **InfluxDB UI:** [http://localhost:8086](http://localhost:8086)
  - Username: `admin`
  - Password: `adminpassword`
  - Organization: `example-org`
  - Bucket: `example-bucket`
  - Admin Token: `admintoken123`
- **Grafana UI:** [http://localhost:3000](http://localhost:3000)
  - Username: `admin`
  - Password: `admin`
  
  [if Grafana WebUI suggests to change password, you can skip it]


## How to Connect Grafana to InfluxDB

1. Log in to Grafana at [http://localhost:3000](http://localhost:3000).
2. Go to **Connections > Add new connection**.
3. Select **InfluxDB > Add new data source**.
4. Set:
   - **URL:** `http://influxdb:8086`
   - **Query Language:** Flux
   - **Auth:** Basic auth
   - **Organization:** `example-org`
   - **Token:** `admintoken123`
   - **Default Bucket:** `example-bucket`
5. Click **Save & Test**. You should see a success message.


## Visualizing Data in Grafana

After connecting your InfluxDB data source in Grafana:

1. **Create a new Dashboard** and add a new Panel.
2. **In the Query section:**
   - Select your InfluxDB data source.
   - Use the Query Builder or switch to the **Flux** editor.
   - Paste the following sample query (adjust the bucket name if needed):

     ```
     from(bucket: "example-bucket")
       |> range(start: -30d)
       |> filter(fn: (r) => r._measurement == "airSensors")
       |> filter(fn: (r) => r._field == "temperature")
       |> aggregateWindow(every: 1h, fn: mean)
       |> yield()
     ```
   - Then click to "Query Inspector" button
   - Then click the "Refresh" button, and close the pop-up window.
   - You should see a line graph with temperature data if the sample data is loaded.

3. More **simple examples:**

   - Raw recent points (quick check): shows any data in the bucket for the last hour.
   ```
   from(bucket: "example-bucket")
    |> range(start: -1h)
    |> limit(n: 50)
    ```

   - Temperature points (raw): narrow to the measurement + field (no aggregation).
   ```
   from(bucket: "example-bucket")
    |> range(start: -24h)
    |> filter(fn: (r) => r._measurement == "airSensors" and r._field == "temperature")
    |> limit(n: 100)
    ```

   - Hourly average (small aggregation): a simpler version of your original query
   ```
   from(bucket: "example-bucket")
    |> range(start: -30d)
    |> filter(fn: (r) => r._measurement == "airSensors" and r._field == "temperature")
    |> aggregateWindow(every: 1h, fn: mean)
   ```

## Stopping and cleaning (start from scratch)

If you want to stop the stack and remove all containers, images and data so the next `up` starts from a fresh state, follow the commands below.

- Using Docker Compose: this stops services, removes containers, networks, images that were built by Compose, and deletes named volumes created by the compose file. WARNING: deleting volumes will permanently remove the database contents.

In order to stop the execution, please press CTRL+C, and then

```powershell
cd C:\Users\<your path>\Documents\mysql-docker-demo
docker compose down --rmi all -v --remove-orphans
```

- What the flags do:
	- `--rmi all`: removes images built by Compose (your `classicmodels-mysql` image created by `build`).
	- `-v`: removes named volumes declared in `docker-compose.yml` (this deletes DB data).
	- `--remove-orphans`: removes containers from previous runs that are not defined in this compose file.

## Notes

- All data is persisted in Docker volumes (`influxdb_data`, `grafana_data`).