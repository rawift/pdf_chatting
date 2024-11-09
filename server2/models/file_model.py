from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from server2.database import Base


class FileMetadata(Base):
    __tablename__ = "files"
    
    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(255), nullable=False, index=True)  # Matches VARCHAR(255) in SQL
    file_url = Column(Text, nullable=False)  # Matches TEXT in SQL
    mime_type = Column(String(50), nullable=False)  # Matches VARCHAR(50) in SQL
    size = Column(Integer, nullable=False)  # Matches INTEGER in SQL
    created_at = Column(DateTime, default=datetime.utcnow)  # Matches TIMESTAMP with default