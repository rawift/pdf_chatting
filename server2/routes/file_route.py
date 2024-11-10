from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from sqlalchemy.orm import Session
from server2.controllers.file_controller import upload_file_to_db, fetch_latest_file_and_answer
from server2.database import SessionLocal
from server2.schemas.file_schema import FileResponse
from server2.schemas.question import QuestionRequest


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/upload", response_model=FileResponse)
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):

    if file.content_type != 'application/pdf':
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    
    print("upload route")

    file_metadata = upload_file_to_db(file, db)

    if not file_metadata:
        raise HTTPException(status_code=500, detail="Failed to upload file to database.")
    

    response_data = FileResponse(
        file_name=file_metadata.file_name,
        file_url=file_metadata.file_url,
        size=file_metadata.size,
        mime_type=file_metadata.mime_type,
    )
    
    return response_data


@router.post("/question")
async def get_latest_file_answer(request: QuestionRequest, db: Session = Depends(get_db)):

    answer = fetch_latest_file_and_answer(db, request.question)
    

    return {"answer": answer}
