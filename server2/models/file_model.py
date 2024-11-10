from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from server2.database import Base


class FileMetadata(Base):
    __tablename__ = "files"
    
    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(255), nullable=False, index=True)  
    file_url = Column(Text, nullable=False)  
    mime_type = Column(String(50), nullable=False)  
    size = Column(Integer, nullable=False)  
    created_at = Column(DateTime, default=datetime.utcnow)  