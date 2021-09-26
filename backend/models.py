from pydantic import BaseModel


class Epic(BaseModel):
    label: str
    value: int
    disabled: bool = False
