from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
import os
from main import process_query

app = FastAPI()

# Correctly mount the static directory with the URL path and directory path
app.mount("/static", StaticFiles(directory="D:/CODING/StockVietNam/.venv/GUI/static"), name="static")

@app.get("/", response_class=FileResponse)
async def get_chat(request: Request):
    file_path = "D:/CODING/StockVietNam/.venv/GUI/templates/chat.html"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return HTMLResponse(content="File not found", status_code=404)

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
async def handle_query(request: QueryRequest):
    user_input = request.query
    response = process_query(user_input)
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
