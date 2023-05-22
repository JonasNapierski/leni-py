from pydantic import BaseModel


class RequestText(BaseModel):
    msg: str
