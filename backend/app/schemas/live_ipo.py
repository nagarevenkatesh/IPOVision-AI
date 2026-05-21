from pydantic import BaseModel


class SyncResponse(BaseModel):
    saved: int
    total_fetched: int