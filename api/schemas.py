from pydantic import BaseModel

class MessageSearchResponse(BaseModel):
    message_id: str
    message_text: str
    view_count: int
    channel_name: str