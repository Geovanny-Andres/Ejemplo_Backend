from typing import List #Se utiliza para especificar que una función devolverá una lista de elementos
from sqlalchemy.orm import Session #Representa una sesión de base de datos utilizada para interactuar con la base de datos
from fastapi import APIRouter, Depends, HTTPException, status #APIRouter:Una herramienta FastAPI para crear grupos modulares de rutas. Depends:Se utiliza para la inyección de dependencia, lo que permite que las funciones reciban las dependencias requeridas automáticamente. HTTPException:Se utiliza para generar errores HTTP, como 404 No encontrado. status:Contiene códigos de estado HTTP para facilitar la lectura.
import schemas #Contiene los modelos de Pydantic (validación de datos).
import crud #Contiene las funciones principales para crear, leer, actualizar y eliminar elementos "pendientes".
from database import SessionLocal #Una fábrica de sesiones database.py utilizada para interactuar con la base de datos.

#Crea el Enrutador
router = APIRouter(
    prefix="/todos" #Prefijo de URL /todos. Todas las rutas definidas en este enrutador comenzarán con /todos.
)

#Dependencia para la sesión de base de datos
def get_db(): #Proporciona sesión de base de datos a las rutas
    db = SessionLocal()
    try:
        yield db #Abre una conexión a la base de datos
    finally:
        db.close()

#Crea un elemento
@router.post("", status_code=status.HTTP_201_CREATED) #Define una solicitud POST en el /todos endpoint
def create_todo(todo: schemas.ToDoRequest, db: Session = Depends(get_db)): #El cuerpo de la solicitud debe coincidir con el ToDoRequest esquema. Se inyecta la sesión de base de datos
    todo = crud.create_todo(db, todo)
    return todo #Devuelve el elemento creado

#Obtener los elementos
@router.get("", response_model=List[schemas.ToDoResponse]) #Recupera elementos filtrando por estado de finalización. Define una solicitud GET
def get_todos(completed: bool = None, db: Session = Depends(get_db)): #Parámetro de consulta opcional para filtrar por estado
    todos = crud.read_todos(db, completed)
    return todos

#Obtener un elemento por ID
@router.get("/{id}") #Define solicitud GET por ID
def get_todo_by_id(id: int, db: Session = Depends(get_db)):
    todo = crud.read_todo(db, id)
    if todo is None:
        raise HTTPException(status_code=404, detail="to do not found") #Genera un error 404 si no lo encuentra
    return todo

#Actualiza un elemento
@router.put("/{id}") #Define una solicitud PUT
def update_todo(id: int, todo: schemas.ToDoRequest, db: Session = Depends(get_db)):
    todo = crud.update_todo(db, id, todo)
    if todo is None:
        raise HTTPException(status_code=404, detail="to do not found") #Actualiza o genera error si no se encuentra
    return todo

#Elimina un elemento
@router.delete("/{id}", status_code=status.HTTP_200_OK) #Define una solicitud DELETE por ID
def delete_todo(id: int, db: Session = Depends(get_db)):
    res = crud.delete_todo(db, id)
    if res is None:
        raise HTTPException(status_code=404, detail="to do not found") #Mensaje de éxito si se elimina o error si no se encuentra