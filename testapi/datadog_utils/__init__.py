import os
import sys
from flask import Flask
from ddtrace import tracer

from testapi.datadog_utils.metrics_prometheus import setup_metrics
from testapi.datadog_utils.errors import add_datadog_spans
from testapi.datadog_utils.trace import ErrorFilter
from testapi.datadog_utils.logger import datadog_logger
from testapi.datadog_utils.metrics_statsd import datadog_metrics


def init_app(app: Flask) -> None:
    datadog_metrics.default_tags = {
        "environment": app.env
    }
    setup_metrics(app)

    tracer.configure(
        hostname=os.environ.get('DD_AGENT_HOST'),
        port=8126,
        settings={'FILTERS': [ErrorFilter()]}
    )

    @app.errorhandler(Exception)
    def add_datadog_spans(e):
        span = tracer.start_span('...')
        curr_span = tracer.current_span()
        curr_span.set_exc_info(
            *sys.exc_info()
        )  # returns type, value (aka the message), traceback which defines the error.type, error.message and error.stack
        return e
