from sqlalchemy.orm import Session #Representa una sesión de base de datos, que se utiliza para interactuar con la base de datos
import models, schemas # models contiene los modelos SQLAlchemy, que se asignan a las tablas de la base de datos. Schemas contiene los esquemas de Pydantic, que definen la estructura de los datos que se pasan (como ToDoRequest).

#Crea un Elemento
def create_todo(db: Session, todo: schemas.ToDoRequest): #Convierte el ToDoRequest esquema (que contiene el nombre y el estado completado) en un ToDo objeto modelo
    db_todo = models.ToDo(name=todo.name, completed=todo.completed)
    db.add(db_todo) #Agrega este nuevo objeto a la sesión de la base de datos.
    db.commit() #Guarda los cambios en la base de datos
    db.refresh(db_todo) #Actualiza el db_todo objeto con cualquier dato nuevo (como los generados automáticamente id).
    return db_todo #Devuelve el ToDo objeto recién creado.

#Lee los elementos
def read_todos(db: Session, completed: bool): #Recupera todos los elementos "pendientes" de la base de datos, filtrando opcionalmente por su estado completado
    if completed is None:
        return db.query(models.ToDo).all() #Devuelve todos los elementos pendientes
    else:
        return db.query(models.ToDo).filter(models.ToDo.completed == completed).all() #Si completed es True o False, filtra los resultados para devolver solo aquellos que coincidan con el estado completado indicado.

#Lee un solo elemento
def read_todo(db: Session, id: int): #Recupera un solo elemento
    return db.query(models.ToDo).filter(models.ToDo.id == id).first() #Busca y retorna el primer elemento por ID que coincida con el indicado o None si no existe.

#Actualiza un elemento
def update_todo(db: Session, id: int, todo: schemas.ToDoRequest): #Actualiza un elemento pendiente
    db_todo = db.query(models.ToDo).filter(models.ToDo.id == id).first() #Busca el elemento
    if db_todo is None: #Si no se encuentra ningún elemento, devuelve None
        return None
    db.query(models.ToDo).filter(models.ToDo.id == id).update({'name': todo.name, 'completed': todo.completed}) #Si el elemento existe actualiza 
    db.commit() #Guarda los cambios en la base de datos
    db.refresh(db_todo) #Actualiza
    return db_todo #Devuelve el elemento actualizado

#Elimina elemento
def delete_todo(db: Session, id: int):
    db_todo = db.query(models.ToDo).filter(models.ToDo.id == id).first() #Busca el elemento por ID
    if db_todo is None: #Si no existe devuelve None
        return None
    db.query(models.ToDo).filter(models.ToDo.id == id).delete() #Si existe lo elimina
    db.commit() #Actualiza
    return True #Confirma que la eliminación fue exitosa