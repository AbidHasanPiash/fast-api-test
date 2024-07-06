from pydantic import BaseModel

class Item(BaseModel):
    id: int = None
    name: str
    description: str
