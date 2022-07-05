import logging

from flask import Flask, jsonify, current_app

from metrics_statsd import datadog_metrics

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
datadog_metrics.default_tags = {
    "environment": app.env
}


@app.route("/")
def hello():
    config_json = {k: str(v) for k, v in current_app.config.items()}
    return jsonify(config_json)


@app.route("/raise")
def raise_exception():
    raise Exception("Exception message")


@app.route("/sdmetrics_incr/<count>")
def statsd_metrics_incr(count: str):
    count = float(count)
    datadog_metrics.incr(
        'test_metric.increment',
        count
    )
    return jsonify({})


@app.route("/sdmetrics_decr/<count>")
def statsd_metrics_decr(count: str):
    count = float(count)
    datadog_metrics.decr(
        'test_metric.increment',
        count
    )
    return jsonify({})


@app.route("/sdmetrics_gauge/<value>")
def statsd_metrics_gauge(value: str):
    value = float(value)
    datadog_metrics.gauge(
        stat='test_metric.gauge',
        value=value,
    )
    return jsonify({})


@app.route("/sdmetrics_set/<value>")
def statsd_metrics_set(value: str):
    value = float(value)
    datadog_metrics.set(
        stat='test_metric.set',
        value=value
    )
    return jsonify({})


if __name__ == "__main__":
    app.run(host="0.0.0.0")
