from pydantic import BaseModel #Se utiliza BaseModel para definir modelos de datos que gestionan automáticamente la validación y serialización de datos (convirtiendo objetos de Python a JSON y viceversa).

class ToDoRequest(BaseModel): #Esta clase define la estructura de los datos cuando se crea o actualiza un nuevo elemento "por hacer"
    name: str #Esto indica que cada elemento "por hacer" debe tener un name, que es una cadena.
    completed: bool #Esto indica si el elemento "por hacer" se completó o no, lo cual es un valor booleano (True o False).

class ToDoResponse(BaseModel): #Esta clase define la estructura de datos cuando se envía un elemento "por hacer" desde el servidor, como cuando se recupera un elemento "por hacer" de la base de datos.
    name: str #El nombre del elemento "por hacer".
    completed: bool #Indica si el elemento "pendiente" está completado.
    id: int #Un identificador único para el elemento "por hacer", que normalmente es generado por la base de datos.

    class Config: #La Configclase con orm_mode = True es una configuración especial para la ToDoResponse clase.
        orm_mode = True #Pydantic permite que la ToDoResponse clase funcione sin problemas con datos provenientes de un ORM (Mapeo Objeto-Relacional) como SQLAlchemy.