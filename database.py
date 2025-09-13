import os #Este módulo proporciona una forma de interactuar con el sistema operativo, particularmente para acceder a las variables de entorno
from sqlalchemy import create_engine #Este es el paquete principal de SQLAlchemy, que se utiliza para conectarse e interactuar con la base de datos
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv #Una función del dotenv paquete que carga variables de entorno desde un .env archivo en su programa.

load_dotenv() #Esta línea carga variables de entorno desde un .env archivo. Estas variables suelen incluir información confidencial, como credenciales de la base de datos (usuario, contraseña), que no conviene codificar directamente.

#SQLALCHEMY_DATABASE_URL = f"postgresql://{os.environ['DATABASE_USER']}:@{os.environ['DATABASE_HOST']}/{os.environ['DATABASE_NAME']}"

#Estas líneas recuperan los detalles de conexión a la base de datos (como nombre de usuario, contraseña, host, puerto y nombre de la base de datos) de las variables de entorno cargadas. Estos valores se almacenan en variables que se utilizarán para crear la cadena de conexión a la base de datos.
user = os.environ['DATABASE_USER']
password = os.environ['DATABASE_PASSWORD']
host = os.environ['DATABASE_HOST']
port = os.environ['DATABASE_PORT']
db_name = os.environ['DATABASE_NAME']

#Construcción de la URL de la base de datos 
#esta URL es como la dirección que SQLAlchemy utilizará para encontrar y conectarse a su base de datos específica.
SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"

engine = create_engine( #Crea un motor que se encarga de gestionar la conexión a la base de datos. Es el punto de partida para cualquier interacción con la base de datos mediante SQLAlchemy.
    SQLALCHEMY_DATABASE_URL
)
# Esta línea crea una fábrica de sesiones
# autocommit=False:Garantiza que las transacciones no se confirmen automáticamente en la base de datos; es necesario confirmarlas explícitamente.
# autoflush=False:Evita el vaciado automático de cambios en la base de datos hasta que se confirmen.
# bind=engine: Vincula la sesión al motor de base de datos que creó anteriormente.

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Esta línea crea una clase base llamada Base, de la que heredarán tus modelos de SQLAlchemy. Esta clase incluye toda la funcionalidad necesaria para mapear clases de Python a tablas de bases de datos.
#Base es como el plano que todos sus modelos de base de datos utilizarán para definir cómo deben lucir las tablas de la base de datos.
Base = declarative_base()