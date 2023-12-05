class CustomException(Exception):
    """
    base exception.
    """

    _status_code: int = 400

    def __init__(self, message: str):
        self.__message = message

    def __str__(self) -> str:
        return self.__message

    @property
    def message(self) -> str:
        return self.__message

    @property
    def status_code(self) -> int:
        return self._status_code


class RequestException(CustomException):
    _status_code: int = 400
    """
    exception for request error.
    """
