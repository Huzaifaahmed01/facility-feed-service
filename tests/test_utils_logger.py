import logging
from app.utils.logger import get_logger


def test_get_logger_returns_logger_instance():
    logger = get_logger("test_logger")
    assert isinstance(logger, logging.Logger)


def test_get_logger_same_name_returns_same_instance():
    logger1 = get_logger("test_logger")
    logger2 = get_logger("test_logger")
    assert logger1 is logger2


def test_get_logger_configures_logger_correctly():
    logger = get_logger("test_logger")
    assert logger.level == logging.INFO
    assert len(logger.handlers) > 0
    handler = logger.handlers[0]
    assert isinstance(handler, logging.StreamHandler)
    assert isinstance(handler.formatter, logging.Formatter)
    # pylint: disable=protected-access
    assert handler.formatter._fmt == (
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
