import functools
import logging


def init_logger():
    logging.config.fileConfig('log/logging.conf')


def log_function_entry_exit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger()
        logger.debug(f"Entering {func.__name__}. Args: {args}, Kwargs: {kwargs}")

        result = func(*args, **kwargs)

        logger.debug(f"Exiting {func.__name__}. Return value: {result}\n")
        return result

    return wrapper
