"""create todos table

Revision ID: ad1c380734f8
Revises: 
Create Date: 2023-12-03 13:25:00.622096

"""
from typing import Sequence, Union #Esto se utiliza para sugerencias de tipo, lo que ayuda a especificar qué tipos pueden ser las variables

from alembic import op #Esto proporciona operaciones (como execute, create_table, etc.) que Alembic puede realizar en la base de datos
import sqlalchemy as sa #Aunque se importa aquí, no se usa directamente en este script. Se usa comúnmente en scripts de migración para definir elementos del esquema de la base de datos


# revision identifiers, used by Alembic.
revision: str = 'ad1c380734f8' #Un identificador único para esta migración. Alembic lo utiliza para rastrearla
down_revision: Union[str, None] = None #Esto indica la migración anterior de la que depende esta. None significa que esta es la primera migración o no depende de una anterior
branch_labels: Union[str, Sequence[str], None] = None # Etiquetas de rama (normalmente None)
depends_on: Union[str, Sequence[str], None] = None # Dependencias de otras revisiones (normalmente None)


def upgrade(): #Es donde se define qué cambios se deben realizar en la base de datos al aplicar esta migración
    op.execute("""       
    create table todos(
        id bigserial primary key,
        name text,
        completed boolean not null default false
    )
    """)
# El comando SQL interno crea una nueva tabla llamada todos con tres columnas:
# id bigserial primary key: Un identificador único para cada fila, incrementado automáticamente por la base de datos (bigserial es un tipo de entero grande que se incrementa automáticamente).
# name text: Una columna de texto para almacenar el nombre del elemento a hacer.
# completed boolean not null default false: Una columna booleana para indicar si el elemento pendiente se completó, con un valor predeterminado de false.


def downgrade(): #función define qué debe suceder si necesita deshacer esta migración
    op.execute("drop table todos;") #Ejecuta un comando SQL sin formato para eliminar la todos tabla. Esto deshace upgrade(), los cambios de la función.
