import logging
import json
import os
import sys
import typing

from flask import has_request_context, request


class JsonFormatter(logging.Formatter):
    """
    Formatter that outputs JSON strings after parsing the LogRecord.

    @param dict fmt_dict: Key: logging format attribute pairs. Defaults to {"message": "message"}.
    @param str time_format: time.strftime() format string. Default: "%Y-%m-%dT%H:%M:%S"
    @param str msec_format: Microsecond formatting. Appended at the end. Default: "%s.%03dZ"
    """

    def __init__(self, fmt_dict: dict = None, time_format: str = "%Y-%m-%dT%H:%M:%S", msec_format: str = "%s.%03dZ"):
        self.fmt_dict = fmt_dict if fmt_dict is not None else {"level": "levelname", "message": "message", "timestamp": "asctime"}
        self.default_time_format = time_format
        self.default_msec_format = msec_format
        self.datefmt = None

    def usesTime(self) -> bool:
        """
        Overwritten to look for the attribute in the format dict values instead of the fmt string.
        """
        return "asctime" in self.fmt_dict.values()

    def formatMessage(self, record) -> dict:
        """
        Overwritten to return a dictionary of the relevant LogRecord attributes instead of a string.
        KeyError is raised if an unknown attribute is provided in the fmt_dict.
        """
        return {fmt_key: record.__dict__[fmt_val] for fmt_key, fmt_val in self.fmt_dict.items()}

    def format(self, record) -> str:
        """
        Mostly the same as the parent's class method, the difference being that a dict is manipulated and dumped as JSON
        instead of a string.
        """
        record.message = record.getMessage()

        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)

        message_dict = self.formatMessage(record)
        message_dict['extra_info'] = {}
        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)

        if record.exc_text:
            message_dict['extra_info']["exc_info"] = record.exc_text

        if record.stack_info:
            message_dict['extra_info']["stack_info"] = self.formatStack(record.stack_info)

        message_dict['extra_info']["request"] = {
            "url": request.path,
            "method": request.method,
            "ip": request.environ.get("REMOTE_ADDR"),
            "headers": request.headers,
        }

        return json.dumps(message_dict, default=str)


class DatadogLogger:

    def __init__(
        self,
        default_level: typing.Optional[str] = None,
        default_stream_formater: typing.Optional[logging.Formatter] = None,
        default_file_formater: typing.Optional[logging.Formatter] = None,
        default_filepath: typing.Optional[str] = None
    ):
        self.default_level = self.str_to_log_level(default_level)
        self.default_stream_formatter = default_stream_formater or logging.Formatter('%(asctime)s %(levelname)s:%(message)s')
        self.default_file_formatter = default_file_formater or JsonFormatter()
        self.default_filepath = default_filepath or os.environ.get('LOG_FILE_PATH')

    @property
    def env_log_level_str(self):
        return os.environ.get('LOG_LEVEL').upper()

    def str_to_log_level(self, log_level_str: typing.Optional[str]):
        log_level_str = log_level_str or self.env_log_level_str

        return getattr(logging, log_level_str)

    def get_file_handler(self, level: logging):
        file_handler = logging.FileHandler(self.default_filepath)
        file_handler.setLevel(level)
        file_handler.setFormatter(self.default_file_formatter)
        return file_handler

    def get_stream_handler(self, level):
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(level)
        stream_handler.setFormatter(self.default_stream_formatter)
        return stream_handler

    def get_logger(
        self,
        name: str,
        level_str: typing.Optional[str] = None,
        to_stream: bool = True,
        to_file: bool = True,
    ):
        level = self.str_to_log_level(level_str) if level_str else self.default_level

        logger = logging.getLogger(name)
        logger.setLevel(level)
        if to_file:
            logger.addHandler(
                self.get_file_handler(level=level)
            )
        if to_stream:
            logger.addHandler(
                self.get_stream_handler(level=level)
            )
        return logger

    @staticmethod
    def get_extra_info(request):
        return {'req': request.get_json()}


datadog_logger = DatadogLogger()







