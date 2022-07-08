# DATADOG Flask poc

```bash
$ DD_API_KEY=xxx docker-compose up
```

# Endpoints
## Generate HTTP 500 Error
```bash
$ curl http://localhost:5000/raise
```

```html
<!doctype html>
<html lang=en>
<title>500 Internal Server Error</title>
<h1>Internal Server Error</h1>
<p>The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.</p>
```

## Metrics
```bash
# increment metric test_metric.increment
$ curl http://localhost:5000/sdmetrics_incr/3
# decrement metric test_metric.increment
$ curl http://localhost:5000/sdmetrics_decr/2
# set metric value test_metric.gauge
$ curl http://localhost:5000/sdmetrics_gauge/45
# set metric value test_metric.set (only set a value of 1 !!)
$ curl http://localhost:5000/sdmetrics_set/78
```

# Locust
Using locust you can call all endpoints in batch to simulate traffic on api.

Start locust batch automatically, uncomment locust and locust-worker in docker-compose file.
