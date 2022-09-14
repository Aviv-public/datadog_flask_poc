import sys

from ddtrace import tracer


def add_datadog_spans(error):
    span = tracer.start_span('...')
    curr_span = tracer.current_span()
    curr_span.set_exc_info(
        *sys.exc_info()
    )  # returns type, value (aka the message), traceback which defines the error.type, error.message and error.stack

    return error