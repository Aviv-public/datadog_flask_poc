import typing

from ddtrace import Span
from ddtrace.filters import TraceFilter


class ErrorFilter(TraceFilter):
    def process_trace(self, trace: typing.List[Span]) -> typing.Optional[typing.List[Span]]:
        if not trace:
            return trace

        local_root = trace[0]

        for span in trace[1:]:
            if span.error == 1:  # or any other conditional for finding the relevant child span

                local_root.set_tags({
                    "error.msg": span.get_tag("error.msg"),
                    "error.type": span.get_tag("error.type"),
                    "error.stack": span.get_tag("error.stack"),
                })

                local_root.error = 1
                break

        return trace
