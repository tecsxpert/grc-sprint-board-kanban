import logging
import os

try:
    import structlog
except ImportError:
    structlog = None


class _FallbackLogger:
    def __init__(self, name):
        self._logger = logging.getLogger(name)

    def warning(self, event, **kwargs):
        self._logger.warning("%s %s", event, kwargs)

    def error(self, event, **kwargs):
        self._logger.error("%s %s", event, kwargs)

    def info(self, event, **kwargs):
        self._logger.info("%s %s", event, kwargs)


def configure_logging():
    level = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(level=level, format="%(message)s")
    if structlog is None:
        return
    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(getattr(logging, level, logging.INFO)),
        cache_logger_on_first_use=True,
    )


def get_logger(name):
    if structlog is None:
        return _FallbackLogger(name)
    return structlog.get_logger(name)
