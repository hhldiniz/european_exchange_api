import enum
from typing import Any


class Response:
    def __init__(self, status_code: int, headers: dict[str, str], body: Any):
        self.status_code = status_code
        self.headers = headers
        self.body = body

    def to_dict(self) -> dict[str, Any]:
        return {
            "statusCode": self.status_code,
            "headers": self.headers,
            "body": self.body
        }

class CommonHeaders(enum.Enum):
    ContentType = "Content-Type"

class ResponseCodes(enum.Enum):
    Status200 = (200, "OK")
    Status201 = (201, "Created")
    Status400 = (400, "Bad Request")
    Status500 = (500, "Internal Server Error")
