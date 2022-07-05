import os
import typing
import re

from datadog import initialize as datadog_initialize, statsd as datadog_statsd


NORMALIZE_REG = re.compile(r"_{2,}")


def normalize_tag(value: str) -> str:
    if not value:
        return value
    value = str(value)
    for char in "/-,=@.:?&^! ":
        value = value.replace(char, "_")
    return NORMALIZE_REG.sub("_", value).strip("_")


class DatadogMetrics:
    default_metrics = {}

    def __init__(self):
        options = {
            'statsd_host': os.environ.get('DD_AGENT_HOST'),
            # 'statsd_port': 8125,
        }
        datadog_initialize(**options)
        self.default_tags = {}

    def _tags_dict_to_str(self, dict_tags: typing.Dict[str, str]) -> typing.List[str]:
        return [self._tags_to_str(k, v) for k, v in dict_tags.items()]

    def _tags_to_str(self, tag_key: str, tag_value: str) -> str:
        return "{tag}:{value}".format(tag=tag_key, value=normalize_tag(tag_value))

    def build_tags(self, tags: typing.Optional[typing.Union[dict, list]] = None) -> typing.Optional[typing.List[str]]:
        tags_list = tags or []

        if self.default_tags:
            tags_list = tags_list + self._tags_dict_to_str(self.default_tags)

        if isinstance(tags, dict):
            tags_list = tags_list + self._tags_dict_to_str(tags)

        return tags_list or None

    def incr(
        self,
        stat: str,
        count: float = 1,
        rate: typing.Optional[float] = 1,
        **tags: typing.Optional[str]
    ):
        """Increment a stat by `count`."""
        datadog_statsd.increment(
            metric=stat,
            value=count,
            tags=self.build_tags(tags),
            sample_rate=rate
        )

    def decr(
        self,
        stat: str,
        count: float = -1,
        rate: typing.Optional[float] = 1,
        **tags: typing.Optional[str]
    ):
        """Decrement a stat by `count`."""
        datadog_statsd.decrement(
            metric=stat,
            value=count,  # or -count?
            tags=self.build_tags(tags),
            sample_rate=rate
        )

    def timer(self, stat: str, rate=1, **tags):
        # TODO
        pass

    def gauge(
        self,
        stat: str,
        value: float,
        rate: typing.Optional[float] = 1,
        delta: bool = False,
        **tags: typing.Optional[str]
    ):
        """Set a gauge value."""
        datadog_statsd.gauge(
            metric=stat,
            value=value,
            tags=self.build_tags(tags),
            sample_rate=rate,
            # TODO : delta=delta
        )

    def set(
        self,
        stat: str,
        value: float,
        rate: typing.Optional[float] = 1,
        **tags: typing.Optional[str]
    ):
        datadog_statsd.set(
            metric=stat,
            value=value,
            tags=self.build_tags(tags),
            sample_rate=rate
        )





datadog_metrics = DatadogMetrics()