# Exercise: Visualizing Air Sensor Data with InfluxDB and Grafana

## Objective
Use Grafana to query, visualize, and interpret environmental air sensor data stored in InfluxDB. Gain experience creating dashboards and interpreting time-series data.

## Instructions
1. Ensure Your Stack Is Running
Confirm that both InfluxDB and Grafana are running (e.g., via Docker Compose).

    - InfluxDB UI: http://localhost:8086

    - Grafana UI: http://localhost:3000

2. Confirm Data Availability in InfluxDB
    - Log in to InfluxDB.

    - Go to Data Explore and check that the airSensors measurement exists in your bucket (e.g., example-bucket).

    - Use the Script Editor to run (copy and press the Submit button):
        ```
        from(bucket: "example-bucket")
        |> range(start: -7d)
        |> filter(fn: (r) => r._measurement == "airSensors")
        |> filter(fn: (r) => r._field == "temperature")
        ```
    - If you see data, you’re ready to proceed.

3. Connect Grafana to InfluxDB
In Grafana, go to Connections > Data Sources > Add data source.

    - Choose InfluxDB.

    - Set:

        - URL: http://influxdb:8086

        - Query Language: Flux

        - Organization: example-org

        - Token: admintoken123

        - Default Bucket: example-bucket

        Click Save & Test (you should see a success message).

4. Create a New Dashboard and Panel in Grafana
    - Go to Dashboards > New > New Dashboard.

    - Click Add new panel.

5. Write a Query to Visualize Air Sensor Data
    - In the panel’s Query section, select your InfluxDB data source.

    - Use the Flux query editor and paste:
        ```
        from(bucket: "example-bucket")
        |> range(start: -7d)
        |> filter(fn: (r) => r._measurement == "airSensors")
        |> filter(fn: (r) => r._field == "temperature")
        |> aggregateWindow(every: 1h, fn: mean)
        |> yield()
        ```
    - Adjust the bucket name if needed.

    - Set the dashboard time range (top right) to Last 7 days or All time if you don’t see data.

6. Customize the Visualization
    - Change the visualization type (e.g., line chart, bar chart, table) to best represent the data.

    - Add a title and description to your panel.

    - Experiment by changing the field to humidity or co, or by grouping by sensor_id or location for comparative charts.

7. Experiment Further (Optional)
    - Add additional panels for other fields (humidity, CO).

    - Try grouping by location or sensor for multi-series charts.

    - Use the query builder or Flux script editor for more advanced queries.

8. Save and Present
    - Save your dashboard.


Sample Queries for Grafana

Average Humidity per Hour:
```
from(bucket: "example-bucket")
  |> range(start: -7d)
  |> filter(fn: (r) => r._measurement == "airSensors")
  |> filter(fn: (r) => r._field == "humidity")
  |> aggregateWindow(every: 1h, fn: mean)
  |> yield()
```

Compare Temperature by Sensor:
```
from(bucket: "example-bucket")
  |> range(start: -7d)
  |> filter(fn: (r) => r._measurement == "airSensors")
  |> filter(fn: (r) => r._field == "temperature")
  |> group(columns: ["sensor_id"])
  |> aggregateWindow(every: 1h, fn: mean)
  |> yield()
```


