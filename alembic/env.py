import os # Acceso a variables de entorno (.env cargado abajo). Esta línea se incluye
from logging.config import fileConfig # Inicializa el logging de Alembic usando alembic.ini.

from sqlalchemy import engine_from_config # Crea un Engine SQLAlchemy a partir de la config (sección [alembic]).
from sqlalchemy import pool   # Tipos de pool de conexiones (NullPool = sin reutilización).

from alembic import context # "contexto" de migración: API que orquesta cómo corre Alembic.
from dotenv import load_dotenv # Carga el archivo .env a variables de entorno (os.environ). Esta línea se incluye

load_dotenv()  # Hace disponibles DATABASE_* desde .env (útil para construir la URL). Esta línea se incluye

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
# "config" es el objeto de configuración de Alembic (lee alembic.ini).
# Sirve para consultar/ajustar opciones como sqlalchemy.url, que define a qué BD conectarse.

config = context.config

#config.set_main_option("sqlalchemy.url", f"postgresql://{os.environ['DATABASE_USER']}:@{os.environ['DATABASE_HOST']}:{os.environ['DATABASE_PORT']}/{os.environ['DATABASE_NAME']}")
# URL real de conexión. Nota: si tu contraseña tiene caracteres especiales (@ : / # ? &)
# podrías necesitar codificarla o usar sqlalchemy.engine.URL para construirla de forma segura.
#Esta línea se incluye, el resto viene en el código
config.set_main_option("sqlalchemy.url", f"postgresql://{os.environ['DATABASE_USER']}:{os.environ['DATABASE_PASSWORD']}@{os.environ['DATABASE_HOST']}:{os.environ['DATABASE_PORT']}/{os.environ['DATABASE_NAME']}")

# Configura el sistema de logging de Alembic (según lo definido en alembic.ini).
# Útil para ver en consola qué operaciones ejecuta durante las migraciones.
# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata objetivo para 'autogenerate'.
# Si quieres que Alembic compare modelos vs BD, asigna Base.metadata aquí.
# p. ej.: from models import Base; target_metadata = Base.metadata

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = None

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

# Puedes leer otras opciones del .ini así:
# my_important_option = config.get_main_option("my_important_option")
# (No se usa aquí.)
def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata, # Si fuera Base.metadata, permitiría autogenerate.
        literal_binds=True,  # Inserta literales en vez de parámetros.
        dialect_opts={"paramstyle": "named"}, # Estilo de parámetros del dialecto.
    )

    with context.begin_transaction():
        context.run_migrations()  # Emite el SQL de la revisión


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}), # Lee sección [alembic]
        prefix="sqlalchemy.", # Toma claves que empiecen con sqlalchemy.
        poolclass=pool.NullPool,  # Sin pool: una conexión por corrida
    )

    with connectable.connect() as connection: # Abre la conexión real a la BD.
        context.configure(
            connection=connection, target_metadata=target_metadata  # Usa esta conexión
        )# Con Base.metadata permite autogenerate

        with context.begin_transaction():  # Transacción de migración
            context.run_migrations()  # Ejecuta upgrade/downgrade de la revisión

# Selecciona automáticamente el modo según cómo se invoca Alembic.
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
