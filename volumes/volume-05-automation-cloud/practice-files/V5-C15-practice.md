# Practice Guide: Chapter 15 (Volume 5)

## Objective
To conceptually analyze the JSON structure of a Distributed Trace Span, understanding how Spans link together to form a complete Trace.

## Assignment 1: The Span Structure
When an OpenTelemetry SDK (running inside a Java or Python application) generates a Span, it eventually ships a JSON object to the backend (like Jaeger).

1. **Review this theoretical OpenTelemetry Span JSON:**

    ```json
    {
      "traceId": "4bf92f3577b34da6a3ce929d0e0e4736",
      "spanId": "00f067aa0ba902b7",
      "parentSpanId": "5e2c34a1bc8f921d",
      "name": "SELECT user_profiles",
      "kind": "SPAN_KIND_CLIENT",
      "startTimeUnixNano": 1698765432000000000,
      "endTimeUnixNano": 1698765432150000000,
      "attributes": [
        {
          "key": "http.method",
          "value": {
            "stringValue": "GET"
          }
        },
        {
          "key": "db.system",
          "value": {
            "stringValue": "postgresql"
          }
        },
        {
          "key": "db.statement",
          "value": {
            "stringValue": "SELECT * FROM user_profiles WHERE id = 1234"
          }
        }
      ]
    }
    ```

2. **Analysis of the Identifiers:**
   * `"traceId"`: The globally unique ID for the entire customer transaction. If you search this ID in Jaeger, you will see the whole waterfall graph.
   * `"spanId"`: The unique ID for this specific micro-operation (the SQL query).
   * `"parentSpanId"`: The ID of the Span that triggered this one! Because this Span has a parent, the Jaeger UI knows to draw this Span *underneath* the parent in the visual waterfall graph.

3. **Analysis of the Data:**
   * `"startTimeUnixNano"` and `"endTimeUnixNano"`: By subtracting these two timestamps, the Tracing UI calculates that this exact SQL query took **150 milliseconds**.
   * `"attributes"`: These are key/value tags added by the developer or the auto-instrumentation library. The SRE can see the exact `db.statement` that was executed, making it incredibly easy to hand the slow SQL query to a Database Administrator to optimize!

## Success Criteria
You have successfully completed this practice if you can explain how a Tracing UI (like Jaeger) knows how to draw a complex, nested waterfall graph out of millions of disconnected JSON objects. (Answer: It queries the database for all Spans that share the exact same `traceId`, and then uses the `parentSpanId` fields to link them together hierarchically, building a tree structure!).
