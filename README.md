# DATADOG Flask poc

# Features
- APM enabled
- Trace enabled
- Custom StatsDMetrics
- Logging: applicaton and/or container logs

# TODO
- When Flask is not in debug mode, errors are not reported in Error Tracking (Datadog support ticket in progress)
- StatsD Metrics:
  - [ ] type "set" set value to 1 (instead of metric value)
  - [ ] type "timer" replacement
- Logging
  - Container logs
    - :broken_heart: all logs are reported as info
    - :broken_heart: stacktraces are not grouped 

# Run application

```bash
$ DD_API_KEY=xxx docker-compose up
```

# Generate traffic on Application
## Automatic (Locust)
A locust service is automatically started on launch to generate traffic on application.

View/Monitor locust run at http://localhost:8089/

Disable service, comment the locust services in docker compose file.

## Manual
### Default endoint
```bash
$ curl http://localhost:5000/
```

### Generate HTTP 500 Error
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

### Custom statsd Metrics
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

### Logging
```bash
# generate a debug log
$ curl http://localhost:5000/logging/debug
# generate a info log
$ curl http://localhost:5000/logging/info
# generate a warning log
$ curl http://localhost:5000/logging/warning
# generate a error log
$ curl http://localhost:5000/logging/error
# generate a critical log
$ curl http://localhost:5000/logging/critical
```
> View logs in https://app.datadoghq.eu/logs/livetail

# Logging
## Application logs
The current version of application send application logs to Datadog.
- Application explicit logs are written in a json file (see application logging with a fileHandler)
- Json log file is mounted on datadog-agent (see datadog-agents volumes in docker-compose)
- Datadog-agent read and send logs to Datadog website (see ./datadog-agent-python-logs-conf.yml).


## Container logs
Another option available is to send all application containter logs to Datadog.

In datadog-agent.env
```dotenv
DD_LOGS_CONFIG_CONTAINER_COLLECT_ALL=true
```

In docker-compose
```yaml
      # LOGGING[OPTION2]: enable for logging based on containter autodiscovery
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - /proc/:/host/proc/:ro
      - /sys/fs/cgroup/:/host/sys/fs/cgroup:ro
      - /etc/passwd:/etc/passwd:ro
```

# Datadog DashBoard
## Create a datadog dashboard

```json
{"title":"MA - TestAPI","description":"## Title\n\nDescribe this dashboard. Add links to other dashboards, monitors, wikis,  and docs to help your teammates. Markdown is supported.\n\n- [This might link to a dashboard](#)\n- [This might link to a wiki](#)","widgets":[{"id":2404946736844091,"definition":{"title":"All Requests by Endpoint","title_size":"16","title_align":"left","show_legend":true,"legend_layout":"horizontal","legend_columns":["avg","min","max","value","sum"],"type":"timeseries","requests":[{"formulas":[{"formula":"query1"}],"response_format":"timeseries","queries":[{"query":"sum:trace.flask.request.hits{service:testapi,env:$env.value} by {resource_name}.as_count()","data_source":"metrics","name":"query1"}],"style":{"palette":"dog_classic","line_type":"solid","line_width":"normal"},"display_type":"line"}]},"layout":{"x":0,"y":0,"width":5,"height":3}},{"id":7174504803456351,"definition":{"title":"All Requests Duration by Endpoint","title_size":"16","title_align":"left","type":"toplist","requests":[{"formulas":[{"formula":"query1","limit":{"count":500,"order":"desc"}}],"response_format":"scalar","queries":[{"query":"sum:trace.flask.request.duration{env:$env.value,service:$service.value} by {resource_name}","data_source":"metrics","name":"query1","aggregator":"avg"}]}]},"layout":{"x":5,"y":0,"width":5,"height":3}},{"id":6639707856466071,"definition":{"title":"All Requests by Endpoint 2XX","title_size":"16","title_align":"left","show_legend":true,"legend_layout":"horizontal","legend_columns":["avg","min","max","value","sum"],"type":"timeseries","requests":[{"formulas":[{"formula":"query1"}],"response_format":"timeseries","queries":[{"query":"sum:trace.flask.request.hits{env:$env.value,service:$service.value,http.status_code:2*} by {resource_name,http.status_code}.as_count()","data_source":"metrics","name":"query1"}],"style":{"palette":"dog_classic","line_type":"solid","line_width":"normal"},"display_type":"line"}]},"layout":{"x":0,"y":3,"width":5,"height":3}},{"id":1511961027831519,"definition":{"title":"All Requests by Endpoint != 2XX","title_size":"16","title_align":"left","show_legend":true,"legend_layout":"horizontal","legend_columns":["avg","min","max","value","sum"],"type":"timeseries","requests":[{"formulas":[{"formula":"query1"}],"response_format":"timeseries","queries":[{"query":"sum:trace.flask.request.hits{env:$env.value,service:$service.value,!http.status_code:2*} by {resource_name,http.status_code}.as_count()","data_source":"metrics","name":"query1"}],"style":{"palette":"dog_classic","line_type":"solid","line_width":"normal"},"display_type":"line"}]},"layout":{"x":5,"y":3,"width":5,"height":3}},{"id":1759063507568562,"definition":{"title":"Custom StatsD metrics","title_size":"16","title_align":"left","show_legend":false,"legend_layout":"auto","legend_columns":["avg","min","max","value","sum"],"time":{"live_span":"15m"},"type":"timeseries","requests":[{"formulas":[{"formula":"query2"},{"formula":"query3"},{"formula":"query4"}],"response_format":"timeseries","queries":[{"query":"sum:test_metric.increment{env:$env.value,service:$service.value}.as_count()","data_source":"metrics","name":"query2"},{"query":"sum:test_metric.gauge{env:$env.value,service:$service.value}","data_source":"metrics","name":"query3"},{"query":"sum:test_metric.set{env:$env.value,service:$service.value}","data_source":"metrics","name":"query4"}],"style":{"palette":"dog_classic","line_type":"solid","line_width":"normal"},"display_type":"line"}]},"layout":{"x":0,"y":6,"width":7,"height":4}}],"template_variables":[{"name":"env","default":"*","prefix":"env","available_values":[]},{"name":"service","default":"testapi","prefix":"service","available_values":["testapi"]}],"layout_type":"ordered","is_read_only":false,"notify_list":[],"reflow_type":"fixed","id":"35u-kpe-bah"}
```
