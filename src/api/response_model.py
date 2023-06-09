from pydantic import BaseModel


class TextResponse(BaseModel):
    """Simplest version of response.
    """
    code: int
    msg: str
