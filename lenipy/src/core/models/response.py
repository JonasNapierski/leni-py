from pydantic import BaseModel


class ResponseCode(BaseModel):
    code: int
