# Practice Guide: Chapter 14 (Volume 5)

## Objective
To conceptually analyze the JSON structure of a Grafana Dashboard, reinforcing the concept of "Dashboards as Code."

## Assignment 1: The Grafana JSON Model
When you build a graph in the Grafana UI, the server is just writing a JSON file in the background.

1. **Review this theoretical Grafana Panel JSON:**

    ```json
    {
      "id": 1,
      "title": "Production Server CPU Usage",
      "type": "timeseries",
      "datasource": "Prometheus-Primary",
      "targets": [
        {
          "expr": "100 - (avg by (instance) (irate(node_cpu_seconds_total{mode='idle'}[5m])) * 100)",
          "legendFormat": "{{instance}}"
        }
      ],
      "gridPos": {
        "h": 8,
        "w": 12,
        "x": 0,
        "y": 0
      }
    }
    ```

2. **Analysis of the Fields:**
   * `"type": "timeseries"`: This tells Grafana to render a standard line graph over time.
   * `"datasource": "Prometheus-Primary"`: This tells Grafana which database to send the query to.
   * `"expr"`: This is the raw PromQL mathematical expression that Grafana will send to Prometheus! (In this case, it calculates active CPU percentage by subtracting the 'idle' time from 100).
   * `"legendFormat": "{{instance}}"`: Instead of showing a massive ugly metric string in the legend, this tells Grafana to only display the server's name (e.g., `web-01`).
   * `"gridPos"`: This defines exactly where the graph sits on the screen (Height, Width, X/Y Coordinates).

## Assignment 2: Dashboard Variables (Templating)
Let's look at how Grafana creates dynamic dropdown menus.

1. **Review this theoretical Variable JSON:**

    ```json
    "templating": {
      "list": [
        {
          "name": "region",
          "type": "query",
          "datasource": "Prometheus-Primary",
          "query": "label_values(node_cpu_seconds_total, region)",
          "multi": true
        }
      ]
    }
    ```

2. **Analysis:**
   * This creates a dropdown menu at the top of the dashboard named `$region`.
   * It populates the dropdown by querying Prometheus for all the available regions (e.g., `us-east-1`, `eu-west-1`).
   * If an engineer selects `us-east-1` from the dropdown, all the panels on the dashboard can use `region="$region"` in their PromQL expressions to instantly filter the data!

## Success Criteria
You have successfully completed this practice if you understand that a Grafana dashboard is just a JSON file containing PromQL expressions, and that committing this JSON to a Git repository is the only way to protect your visualization layer from accidental deletion!
