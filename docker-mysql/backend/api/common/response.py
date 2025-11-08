import time
from typing import Any, Optional, Dict


class ApiResponse:
    """Simple JSON response helper.

    Usage:
      ApiResponse.ok(data) -> dict
      ApiResponse.fail(code, message) -> dict
    """

    @staticmethod
    def _base(code: int, message: str, data: Optional[Any] = None) -> Dict[str, Any]:
        return {
            "code": code,
            "message": message,
            "data": data,
            "timestamp": int(time.time() * 1000),
        }

    @classmethod
    def ok(cls, data: Optional[Any] = None) -> Dict[str, Any]:
        return cls._base(0, "OK", data)

    @classmethod
    def fail(cls, code: int, message: str) -> Dict[str, Any]:
        return cls._base(code, message, None)

