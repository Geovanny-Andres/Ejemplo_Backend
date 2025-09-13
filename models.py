from sqlalchemy import Boolean, Column, ForeignKey, Integer, String #Son los componentes básicos para definir las columnas (campos) en la tabla de su base de datos.
from sqlalchemy.orm import relationship #Esto se utiliza para definir relaciones entre tablas (p. ej., uno a muchos o muchos a muchos). No se utiliza directamente en este fragmento de código, pero suele importarse para modelos más complejos.

from database import Base #Importada desde tu database.py archivo, es la clase base de la que heredarán todos tus modelos. Esta clase vincula el modelo al ORM de SQLAlchemy.


class ToDo(Base): #Esta clase define una tarea pendiente en la base de datos. Al heredar de Base, se convierte en un modelo de SQLAlchemy, lo que significa que se asignará a una tabla de la base de datos.
    __tablename__ = "todos" #Establece el nombre de la tabla en la base de datos como "todos". Esto significa que cuando SQLAlchemy crea la tabla para este modelo, la nombrará como todos.

    id = Column(Integer, primary_key=True, index=True) #Esto define una columna llamada id en la todos tabla. Almacena números enteros
    name = Column(String) #Esto define una columna llamada name en la tabla. Almacena cadenas de texto.
    completed = Column(Boolean, default=False) #La columna completed almacena valores booleanos.Si no se proporciona ningún valor sera false por defecto