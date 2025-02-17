# core/logging/logger.py
import logging
import json
import sys
from typing import Any, Dict
from core.config import core_settings


class Logger:

    def __init__(self, logger_name: str = "ledger_service"):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(core_settings.logging.log_level)

        formatter = logging.Formatter(
            '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "name": "%(name)s", "message": "%(message)s"}',
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(core_settings.logging.log_level)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        if (
            core_settings.logging.log_file
            and core_settings.logging.log_level.upper() != "DEBUG"
        ):
            file_handler = logging.FileHandler(core_settings.logging.log_file)
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def log_operation(self, operation_type: str, user_id: str, details: Dict[str, Any]):
        log_data = {
            "operation_type": operation_type,
            "user_id": user_id,
            "details": details,
        }
        self.logger.info(json.dumps(log_data))

    def log_error(self, error_type: str, user_id: str, error_details: Dict[str, Any]):
        log_data = {
            "error_type": error_type,
            "user_id": user_id,
            "error_details": error_details,
        }
        self.logger.error(json.dumps(log_data))


logger = Logger()
