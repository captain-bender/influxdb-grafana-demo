# InfluxDB + Grafana Docker Demo

This repository provides a ready-to-use Docker Compose stack for InfluxDB 2.x and Grafana. It is ideal for experimentation, teaching, and building dashboards with time-series data.

## Quick Start
1. Clone the Repository
```
git clone https://github.com/captain-bender/influxdb-grafana-demo
cd influxdb-grafana-demo
```

2. Start the Stack

Make sure that you are inside the project's folder (the one that contains `docker-compose.yml`), e.g.
```
cd C:\Users\<your-name>\Documents\influxdb-grafana-demo
```

and then
```
docker compose up -d
```

The first start takes a minute or two: Docker downloads the InfluxDB and Grafana images and builds a small `data-loader` container that fills InfluxDB with sample air-sensor data.

To check that the sample data has been loaded, follow the loader's output:
```
docker compose logs -f data-loader
```
When you see `Sample data loaded successfully!`, press CTRL+C to stop following the logs (the stack keeps running) and continue.

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
   - **Auth:** leave all toggles (including Basic auth) switched off — the token below is used instead
   - **Organization:** `example-org`
   - **Token:** `admintoken123`
   - **Default Bucket:** `example-bucket`
5. Click **Save & Test**. You should see a success message.

> Note: the URL is `http://influxdb:8086`, not `localhost`. Grafana runs in its own container, and inside the Docker network InfluxDB is reached by its service name.


## Visualizing Data in Grafana

After connecting your InfluxDB data source in Grafana:

1. **Create a new Dashboard** and add a new Panel.
2. **Set the time range** (top right of the dashboard) to **Last 7 days**. The sample data covers the 48 hours before the stack was first started, so the default range (Last 6 hours) may show little or nothing.
3. **In the Query section:**
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
   - Click the **Refresh** button above the panel preview.
   - You should see a line graph with one temperature line per sensor.

4. More **simple examples:**

   - Raw points (quick check): shows the first data points in the bucket, whatever they contain.
   ```
   from(bucket: "example-bucket")
    |> range(start: -30d)
    |> limit(n: 50)
   ```

   - Temperature points (raw): narrow to the measurement + field (no aggregation).
   ```
   from(bucket: "example-bucket")
    |> range(start: -30d)
    |> filter(fn: (r) => r._measurement == "airSensors" and r._field == "temperature")
    |> limit(n: 100)
   ```

   - Hourly average (small aggregation): a simpler version of the first query.
   ```
   from(bucket: "example-bucket")
    |> range(start: -30d)
    |> filter(fn: (r) => r._measurement == "airSensors" and r._field == "temperature")
    |> aggregateWindow(every: 1h, fn: mean)
   ```

> Tip: in Grafana you can replace `range(start: -30d)` with `range(start: v.timeRangeStart, stop: v.timeRangeStop)`. The query then follows the dashboard's time picker instead of a fixed window.

## Stopping and cleaning (start from scratch)

To stop the stack but keep your data and dashboards:
```
docker compose down
```

If you want to stop the stack and remove all containers, images and data so the next `up` starts from a fresh state, run the following from inside the project's folder. WARNING: deleting volumes will permanently remove the database contents and your Grafana dashboards.

```powershell
cd C:\Users\<your-name>\Documents\influxdb-grafana-demo
docker compose down --rmi all -v --remove-orphans
```

- What the flags do:
	- `--rmi all`: removes all images used by the stack (InfluxDB, Grafana and the `data-loader` image built by Compose). They will be downloaded/built again on the next `up`. Use `--rmi local` instead to remove only the `data-loader` image and keep the downloaded ones.
	- `-v`: removes named volumes declared in `docker-compose.yml` (this deletes the InfluxDB data and Grafana dashboards).
	- `--remove-orphans`: removes containers from previous runs that are not defined in this compose file.

## Notes

- All data is persisted in Docker volumes (`influxdb_data`, `grafana_data`).
- The `data-loader` runs every time you run `docker compose up`, adding another 48 hours of sample data ending at that moment. Run the clean-up command above if you want a single, fresh data set.
