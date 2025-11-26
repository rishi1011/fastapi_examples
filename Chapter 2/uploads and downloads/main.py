import shutil

from fastapi import FastAPI, File, UploadFile, HTTPException  
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI()

@app.post("/uploadfile")
async def upload_file(
    file: UploadFile = File(...)):

    with open(
        f"uploads/{file.filename}", "wb"
    ) as buffer:
        shutil.copyfileobj(file.file, buffer)   

    return {"filename": file.filename}

@app.get(
    "/downloadfile/{filename}",
    response_class=FileResponse
    )
async def download_file(filename: str):
    if not Path(f"uploads/{filename}").exists():
        raise HTTPException(
            status_code=404,
            detail=f"file {filename} not found."
        )
    
    return FileResponse(
        path=f"uploads/{filename}", filename=filename
    )
