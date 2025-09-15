from dotenv import load_dotenv
load_dotenv()

import os
import sqlite3
from typing import Optional
from datetime import datetime  # Para fecha si hace falta

from openai import OpenAI
from fastapi import FastAPI, HTTPException, status, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ======================================
# Configuración cliente OpenAI / OpenRouter
# ======================================
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    # Si no hay clave, el endpoint IA fallará con excepción controlada más adelante.
    pass

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)

# ======================================
# Inicialización FastAPI
# ======================================
app = FastAPI(title="Micrositio API REST - Productos")

# Permitir CORS (para desarrollo). En producción restringir allow_origins.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================================
# Modelos Pydantic
# ======================================
class Producto(BaseModel):
    nombre: str
    description: Optional[str] = None
    precio: int
    image_url: Optional[str] = None
    video_url: Optional[str] = None

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    description: Optional[str] = None
    precio: Optional[int] = None
    image_url: Optional[str] = None
    video_url: Optional[str] = None

# ======================================
# Función de conexión a la DB
# ======================================
DB_PATH = "miwebsite.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

# ======================================
# Endpoint para crear la BD (tablas)
# ======================================
@app.post("/create-db/")
def create_db():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        # Tabla de productos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                description TEXT,
                precio INTEGER NOT NULL,
                image_url TEXT,
                video_url TEXT
            )
        ''')
        # Tabla de contactos (unificado a 'correo')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contactos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                correo TEXT NOT NULL,
                mensaje TEXT NOT NULL,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        return {"message": "Base de datos y tablas creadas correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear la base de datos: {e}")
    finally:
        conn.close()

# ======================================
# CRUD Productos
# ======================================
@app.post("/productos/")
def crear_producto(producto: Producto):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            '''
            INSERT INTO productos (nombre, description, precio, image_url, video_url)
            VALUES (?, ?, ?, ?, ?)
            ''',
            (producto.nombre, producto.description, producto.precio, producto.image_url, producto.video_url)
        )
        conn.commit()
        producto_id = cursor.lastrowid
        return JSONResponse(
            content={"message": "Producto creado correctamente", "id": producto_id, "data": producto.dict()},
            status_code=status.HTTP_201_CREATED
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el producto: {e}")
    finally:
        conn.close()

@app.get("/productos/")
def listar_productos():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT id, nombre, description, precio, image_url, video_url FROM productos')
        productos = cursor.fetchall()
        return [dict(row) for row in productos]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar productos: {e}")
    finally:
        conn.close()

@app.get("/productos/{producto_id}")
def detalle_producto(producto_id: int):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM productos WHERE id = ?', (producto_id,))
        row = cursor.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return dict(row)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el producto: {e}")
    finally:
        conn.close()

@app.put("/productos/{producto_id}")
def actualizar_producto(producto_id: int, update: ProductoUpdate):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM productos WHERE id = ?', (producto_id,))
        existing = cursor.fetchone()
        if existing is None:
            raise HTTPException(status_code=404, detail="Producto no encontrado")

        fields = []
        values = []
        update_dict = update.dict(exclude_unset=True)  # Solo campos no None
        for key, value in update_dict.items():
            fields.append(f"{key} = ?")
            values.append(value)
        if not fields:
            return {"message": "Nada que actualizar"}
        values.append(producto_id)
        sql = f"UPDATE productos SET {', '.join(fields)} WHERE id = ?"
        cursor.execute(sql, tuple(values))
        conn.commit()
        return {"message": "Producto actualizado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar producto: {e}")
    finally:
        conn.close()

@app.delete("/productos/{producto_id}")
def eliminar_producto(producto_id: int):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM productos WHERE id = ?', (producto_id,))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return {"message": "Producto eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar producto: {e}")
    finally:
        conn.close()

@app.delete("/productos/")
def eliminar_todos():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM productos")
        conn.commit()
        return {"message": "Todos los productos fueron eliminados"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar productos: {e}")
    finally:
        conn.close()

# ======================================
# Endpoint para contactos (corregido con Form)
# ======================================
@app.post("/contacto/")
async def procesar_formulario_contacto(
    nombre: str = Form(...),
    correo: str = Form(...),
    mensaje: str = Form(...)
):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO contactos (nombre, correo, mensaje) VALUES (?, ?, ?)",
            (nombre, correo, mensaje)
        )
        conn.commit()
        return {"message": "Formulario recibido y guardado correctamente."}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al guardar el contacto: {e}"
        )
    finally:
        conn.close()

@app.get("/contacto/")
def listar_contactos():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, correo, mensaje, fecha FROM contactos ORDER BY fecha DESC")
        contactos = cursor.fetchall()
        return [dict(row) for row in contactos]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar contactos: {e}")
    finally:
        conn.close()

# ======================================
# Endpoint IA: significado de un nombre
# ======================================
@app.post("/significado-nombre")
async def obtener_significado(nombre: str = Form(...)):
    if not OPENROUTER_API_KEY:
        raise HTTPException(status_code=500, detail="No se encontró la clave OPENROUTER_API_KEY en .env")

    try:
        respuesta = client.chat.completions.create(
            extra_headers={},
            model="gpt-oss-20b:free",
            messages=[
                {"role": "system", "content": "Eres un experto en Nombres y su significado."},
                {"role": "user", "content": f"¿puedes darme brevemente el significado de {nombre}?"}
            ]
        )
        significado = respuesta.choices[0].message.content.strip()
        return {"nombre": nombre, "significado": significado}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el significado del nombre: {e}")