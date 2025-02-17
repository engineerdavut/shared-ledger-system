# tests/core/logging/test_logger.py
from core.logging.logger import logger


def test_log_operation():

    logger.log_operation("test_operation", "test_user", {"detail": "test detail"})
    assert True


def test_log_error():
    logger.log_error("test_error", "test_user", {"error_detail": "test error detail"})
    assert True
