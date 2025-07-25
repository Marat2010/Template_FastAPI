# core/logger.py.template
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import sys
from typing import Optional

from core.config import settings


class SensitiveDataFilter(logging.Filter):
    """Фильтрация чувствительных данных"""
    def filter(self, record):
        if "password" in record.msg.lower():
            record.msg = "***REDACTED***"
        return True


def setup_logger() -> logging.Logger:
    """Настройка базового логгера с выводом в консоль и файл"""

    logger = logging.getLogger(settings.log.LOGGER_NAME)
    if logger.handlers:  # Уже настроен
        return logger
    logger.setLevel(settings.log.LOG_LEVEL)

    # Форматтер для логов
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Консольный вывод
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Файловый вывод (если указан в настройках)
    if settings.log.LOG_FILE:
        log_path = Path(settings.log.LOG_FILE)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = RotatingFileHandler(
            log_path,
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Фильтр чувствительных данных
    logger.addFilter(SensitiveDataFilter())

    # Перенаправляем логи FastAPI и Uvicorn
    for name in ("uvicorn", "uvicorn.error", "uvicorn.access", "fastapi"):
        lib_logger = logging.getLogger(name)
        lib_logger.handlers = []
        lib_logger.propagate = True  # Пусть логи идут в корневой логгер

    return logger


# Глобальный экземпляр логгера
logger = setup_logger()

