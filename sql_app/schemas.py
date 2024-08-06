from pydantic import BaseModel


class HistoryBase(BaseModel):
    search: str
    suggestions: list[str]


class HistoryCreate(HistoryBase):
    pass


class History(HistoryBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: str
    spotify_id: str


class User(UserBase):
    id: int
    history: list[History] = []

    class Config:
        from_attributes = True
