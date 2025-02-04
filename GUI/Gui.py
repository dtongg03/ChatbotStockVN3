from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

app = FastAPI()

# Configure CORS for GitHub Pages
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=FileResponse)
async def get_chat(request: Request):
    file_path = "./templates/chat.html"
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
