from typing import Optional
import asyncio
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError, OperationalError
from asyncpg.exceptions import CannotConnectNowError, PostgresError
from core.logger import logger


async def wait_for_db(
        engine,
        max_retries: int = 5,
        retry_delay: float = 2.0,
        test_query: str = "SELECT 1"
) -> bool:
    """
    Ожидает доступности базы данных с повторными попытками подключения.

    :param engine: SQLAlchemy async engine
    :param max_retries: Максимальное количество попыток
    :param retry_delay: Задержка между попытками в секундах
    :param test_query: Тестовый запрос для проверки соединения
    :return: True если подключение успешно
    :raises RuntimeError: После исчерпания всех попыток
    """
    last_error: Optional[Exception] = None

    for attempt in range(1, max_retries + 1):
        try:
            async with engine.connect() as conn:
                await conn.execute(text(test_query))
                logger.info("Подключение к БД успешно установлено")
                return True

        except (OperationalError, DBAPIError,
                ConnectionRefusedError, ConnectionError,
                CannotConnectNowError, PostgresError) as e:

            last_error = e
            logger.warning(
                f"Попытка {attempt}/{max_retries}: Не удалось подключиться к БД. "
                f"Ошибка: {type(e).__name__}: {str(e)}"
            )

            if attempt < max_retries:
                logger.info(f"Повторная попытка через {retry_delay} сек...")
                await asyncio.sleep(retry_delay)

    logger.critical(
        f"Не удалось подключиться к БД после {max_retries} попыток. "
        f"Последняя ошибка: {type(last_error).__name__}: {str(last_error)}",
        exc_info=last_error
    )
    raise RuntimeError(
        f"Database connection failed after {max_retries} attempts. "
        f"Last error: {str(last_error)}"
    ) from last_error
