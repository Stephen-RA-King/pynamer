# Core Library modules
from typing import Any, Callable

# Third party modules
from requests import (
    ConnectionError,
    HTTPError,
    RequestException,
    Timeout,
    TooManyRedirects,
)

# Local modules
from . import logger


def request_exception(func: Callable) -> Callable:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            result = func(*args, **kwargs)
        except ConnectionError as e:  # pragma: no cover
            logger.error("A connection error occurred: %s", e)
            raise SystemExit("A connection error occurred") from e
        except TooManyRedirects as e:  # pragma: no cover
            logger.error("Too many redirects occurred: %s", e)
            raise SystemExit("Too many redirects occurred") from e
        except Timeout as e:  # pragma: no cover
            logger.error("The request timed out: %s", e)
            raise SystemExit("The request timed out") from e
        except HTTPError as e:  # pragma: no cover
            logger.error("An HTTP error occurred.: %s", e)
            raise SystemExit("An HTTP error occurred.") from e
        except RequestException as e:  # pragma: no cover
            logger.error(
                "An ambiguous exception occurred while handling request: %s",
                e,
            )
            raise SystemExit(
                "An ambiguous exception occurred while handling request."
            ) from e
        return result

    return wrapper


def file_exception(func: Callable) -> Callable:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            result = func(*args, **kwargs)
        except FileNotFoundError as e:  # pragma: no cover
            logger.error("The file does not exist: %s", e)
            raise SystemExit("The file does not exist") from e
        except PermissionError as e:  # pragma: no cover
            logger.error("Permission denied to file: %s", e)
            raise SystemExit("Permission denied to file") from e
        except IsADirectoryError as e:  # pragma: no cover
            logger.error("File is a directory not a file: %s", e)
            raise SystemExit("File is a directory not a file") from e
        except OSError as e:  # pragma: no cover
            logger.error("A general IO error has occurred opening file: %s", e)
            raise SystemExit("A general IO error has occurred opening file") from e
        except Exception as e:  # pragma: no cover
            logger.error("An error occurred: %s", e)
            raise SystemExit("An error occurred") from e
        return result

    return wrapper
