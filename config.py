from pydantic_settings import BaseSettings # BaseSettings se utiliza para crear clases de configuración que pueden leer y validar variables de entorno y .env

class Settings(BaseSettings): # La clase Settings hereda de BaseSettings. Esto significa que todos los atributos definidos en esta clase se considerarán configuraciones que pueden completarse mediante variables de entorno.
    DATABASE_HOST: str # Host de Postgres (ej. "localhost")
    DATABASE_NAME: str # Nombre de la base (ej. "database082724")
    DATABASE_USER: str # Usuario de la base (ej. "todo_user")
    DATABASE_PASSWORD: str # Contraseña del usuario
    DATABASE_PORT: int # Puerto (ej. 5432)
    app_name: str = "Full Stack To Do App" # Valor por defecto si no está en .env

    class Config: # Es una clase especial que se utiliza para configurar cómo pydantic_settings debe comportarse
        env_file = ".env" # Indica que lea variables del archivo .env
        extra = "ignore"  # Ignora claves extra no declaradas arriba
