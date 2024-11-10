import os
from fastapi import HTTPException
import getpass
import warnings
from sqlalchemy.orm import Session
from server2.models.file_model import FileMetadata

from server2.schemas.file_schema import FileResponse
from server2.langchain import pdf_qa_function

from server2.s3_utils import upload_to_s3



from langchain_community.document_loaders import PyPDFLoader




def upload_file_to_db(file, db: Session):

    file_size = len(file.file.read())
    file.file.seek(0)  
    

    s3_url = upload_to_s3(file, "aissigments")
    
    
    file_name = file.filename
    mime_type = file.content_type

    file_metadata = FileMetadata(
        file_name=file_name,
        file_url=s3_url,
        mime_type=mime_type,
        size=file_size
    )
  
    db.add(file_metadata)
    db.commit()
    db.refresh(file_metadata)

    return file_metadata



try:
    from langchain.chains import ConversationalRetrievalChain
except ImportError:
    raise ImportError("ConversationalRetrievalChain is not available in your version of LangChain. "
                      "Please update or check documentation for alternatives.")


def fetch_latest_file_and_answer(db: Session, question: str):

    latest_file = db.query(FileMetadata).order_by(FileMetadata.created_at.desc()).first()
    if not latest_file:
        raise HTTPException(status_code=404, detail="No files found.")


    file_path = latest_file.file_url
    loader = PyPDFLoader(file_path)

    docs = loader.load()
 
    answer = pdf_qa_function(question,file_path)

    print(answer)
    return answer['output_text']


    