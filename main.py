from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Libro(BaseModel):
    titulo: str
    autor: str
    paginas: int
    editorial: Optional[str]

#Decorador
@app.get("/")
def index():
    return {"message" : "Hello, World!"}

@app.get("/libros/{id}")
def mostrar_libro(id: int):
    return {"data": id}

@app.post("/libros/")
def crear_libro(libro: Libro):
    return {"message": f"Libro {libro.titulo} ha sido creado"}