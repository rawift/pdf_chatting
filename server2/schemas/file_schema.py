from pydantic import BaseModel
from datetime import datetime

class FileResponse(BaseModel):
    file_name: str
    file_url: str
    size: int 
    mime_type: str 
  

    class Config:
        orm_mode = True
