from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="Projeto PDI")

# Servir os arquivos estáticos do frontend (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("frontend/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/process")
async def process_image(
    image: UploadFile = File(...),
    operation: str = Form(...)
):
    # TODO: Processamento real usando OpenCV
    # O arquivo core.py será chamado aqui
    return {"message": "Image received", "operation": operation, "filename": image.filename}
