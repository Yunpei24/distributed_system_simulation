from pydantic import BaseModel


class Fruit(BaseModel):
    fruit: str

class INGREDIENT(BaseModel):
    id: int
    fruit: str
    execution_time: int