import csv
import os
from fastapi import FastAPI, Request
from fastapi.params import Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class RegistroUsuario(BaseModel):
    nombre: str
    email: EmailStr
    edad: int

CSV_FILE = "usuarios.csv"
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["nombre", "email", "edad"])

@app.get("/", response_class=HTMLResponse)
async def landing_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/registro")
async def registrar_usuario(request: Request, nombre: str = Form(...), edad: int = Form(...), email: str = Form(...)):
    try:
        usuario = RegistroUsuario(nombre = nombre, email=email, edad=edad)
        
        # Guardar en CSV
        with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([usuario.nombre, usuario.email, usuario.edad])
            
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "message": f"¡Felicidades {usuario.nombre}! Registro exitoso."
        })
    except Exception:
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "error": "Por favor, verifica el nombre, edad y correo."
        })