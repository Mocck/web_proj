import time
from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel

class ApiResponse(BaseModel):
    code: int
    message: str
    data: Optional[Any] = None
    timestamp: int

    @classmethod
    def ok(cls, data: Optional[Any] = None):
        return cls(
            code=0,
            message="OK",
            data=data,
            timestamp=int(time.time() * 1000)
        )

    @classmethod
    def fail(cls, code: int, message: str):
        return cls(
            code=code,
            message=message,
            data=None,
            timestamp=int(time.time() * 1000)
        )
