from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid

app = FastAPI(title="API de Notas", version="1.0.0")

# Configurar CORS para permitir conexiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos de datos
class NotaBase(BaseModel):
    titulo: str
    contenido: str
    etiquetas: Optional[List[str]] = []

class NotaCreate(NotaBase):
    pass

class Nota(NotaBase):
    id: str
    fecha_creacion: datetime
    fecha_actualizacion: datetime

# Almacenamiento en memoria (simula una base de datos)
notas_db = {}

# Endpoints
@app.get("/")
def read_root():
    return {"message": "API de Notas funcionando"}

@app.get("/notas", response_model=List[Nota])
def obtener_notas():
    return list(notas_db.values())

@app.get("/notas/{nota_id}", response_model=Nota)
def obtener_nota(nota_id: str):
    if nota_id not in notas_db:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    return notas_db[nota_id]

@app.post("/notas", response_model=Nota)
def crear_nota(nota: NotaCreate):
    nota_id = str(uuid.uuid4())
    ahora = datetime.now()
    
    nueva_nota = Nota(
        id=nota_id,
        titulo=nota.titulo,
        contenido=nota.contenido,
        etiquetas=nota.etiquetas,
        fecha_creacion=ahora,
        fecha_actualizacion=ahora
    )
    
    notas_db[nota_id] = nueva_nota
    return nueva_nota

@app.put("/notas/{nota_id}", response_model=Nota)
def actualizar_nota(nota_id: str, nota_actualizada: NotaCreate):
    if nota_id not in notas_db:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    
    nota_existente = notas_db[nota_id]
    
    nota_actualizada_obj = Nota(
        id=nota_id,
        titulo=nota_actualizada.titulo,
        contenido=nota_actualizada.contenido,
        etiquetas=nota_actualizada.etiquetas,
        fecha_creacion=nota_existente.fecha_creacion,
        fecha_actualizacion=datetime.now()
    )
    
    notas_db[nota_id] = nota_actualizada_obj
    return nota_actualizada_obj

@app.delete("/notas/{nota_id}")
def eliminar_nota(nota_id: str):
    if nota_id not in notas_db:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    
    del notas_db[nota_id]
    return {"message": "Nota eliminada correctamente"}

# Datos de ejemplo para empezar
@app.on_event("startup")
def crear_datos_ejemplo():
    if not notas_db:
        ahora = datetime.now()
        notas_ejemplo = [
            Nota(
                id=str(uuid.uuid4()),
                titulo="Nota de bienvenida",
                contenido="¡Bienvenido a tu aplicación de notas! Puedes crear, editar y eliminar notas.",
                etiquetas=["bienvenida", "información"],
                fecha_creacion=ahora,
                fecha_actualizacion=ahora
            ),
            Nota(
                id=str(uuid.uuid4()),
                titulo="Lista de compras",
                contenido="- Leche\n- Pan\n- Frutas\n- Verduras",
                etiquetas=["compras", "personal"],
                fecha_creacion=ahora,
                fecha_actualizacion=ahora
            ),
            Nota(
                id=str(uuid.uuid4()),
                titulo="Ideas para proyecto",
                contenido="Desarrollar una aplicación web completa con React y FastAPI",
                etiquetas=["trabajo", "proyectos"],
                fecha_creacion=ahora,
                fecha_actualizacion=ahora
            )
        ]
        
        for nota in notas_ejemplo:
            notas_db[nota.id] = nota

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)