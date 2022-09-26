import os

from ddtrace import tracer
from flask import Flask, jsonify, current_app, request

from testapi.datadog_utils.metrics_prometheus import CUSTOM_PROMETHEUS_COUNT
from testapi.datadog_utils.metrics_statsd import datadog_metrics
from testapi.datadog_utils.logger import datadog_logger
from testapi.datadog_utils import init_app as init_datadog


def create_app(name: str = __name__):
    new_application = Flask(os.environ.get('APP_NAME', name))
    init_datadog(new_application)
    return new_application


app = create_app()
logger = datadog_logger.get_logger(name=__name__)


@app.route("/")
@tracer.wrap(name='home_hello')
def hello():
    config_json = {k: str(v) for k, v in current_app.config.items()}
    return jsonify(config_json)


@app.route("/server_error/")
def server_error():
    logger.error("Internal Server error with: Exception message")
    # Note: exception does not generate error log
    raise Exception("Exception message")


@app.route("/error_reponse/<error_code>")
def client_error(error_code: str):
    error_code = int(error_code)
    logger.warning(f"Client error {error_code}")
    return jsonify({"error": error_code}), error_code


@app.route("/sdmetrics_incr/<count>")
def statsd_metrics_incr(count: str):
    count = float(count)
    logger.info(f"Increment metric test_metric.increment to {count}")
    datadog_metrics.incr(
        'test_metric.increment',
        count
    )
    return jsonify({})


@app.route("/sdmetrics_decr/<count>")
def statsd_metrics_decr(count: str):
    count = float(count)
    logger.info(f"Decrement metric test_metric.increment to {count}")
    datadog_metrics.decr(
        'test_metric.increment',
        count
    )
    return jsonify({})


@app.route("/sdmetrics_gauge/<value>")
def statsd_metrics_gauge(value: str):
    value = float(value)
    logger.info(f"Gauge metric test_metric.gauge to {value}")
    datadog_metrics.gauge(
        stat='test_metric.gauge',
        value=value,
    )
    return jsonify({})


@app.route("/sdmetrics_set/<value>")
def statsd_metrics_set(value: str):
    value = float(value)
    logger.info(f"Set metric test_metric.set to {value}")
    datadog_metrics.set(
        stat='test_metric.set',
        value=value
    )
    return jsonify({})


@app.route("/logging/<level>")
@tracer.wrap(name='logger_route')
def logger_test(level: str):
    log_level_mapping = {
        "info": logger.info,
        "warning": logger.warning,
        "critical": logger.critical,
        "error": logger.error,
        "exception": logger.exception,
    }
    logger_func = log_level_mapping.get(level, logger.debug)
    logger_func(
        'logger route was executed',
        extra={
            'extra_info': request.json,
        }
    )
    return jsonify({})


@app.route("/prometheus_counter_inc/<count_type>/<value>")
def prometheus_counter_inc(count_type: str, value: str):
    CUSTOM_PROMETHEUS_COUNT.labels(
        type=count_type,
        value=value,
    ).inc()
    return jsonify({})


if __name__ == "__main__":
    app.run(host="0.0.0.0")
