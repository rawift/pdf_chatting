from pydantic import BaseModel
from datetime import datetime

class FileResponse(BaseModel):
    file_name: str
    file_url: str
    size: int  # Assuming size is an integer representing file size in bytes
    mime_type: str  # MIME type of the file
  

    class Config:
        orm_mode = True
