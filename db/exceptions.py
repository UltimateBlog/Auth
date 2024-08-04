from typing import Optional


class NotFound(Exception):
    def __init__(self, message: Optional[str] = None):
        if message is None:
            message = "Record Not Found"
        super().__init__(message)
