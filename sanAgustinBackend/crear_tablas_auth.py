from sqlalchemy import create_engine
from models.auth_models import Base as AuthBase
from main import Base

# Crear engine
SQLALCHEMY_DATABASE_URL = "sqlite:///./comunidad.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Crear todas las tablas
def crear_tablas():
    print("Creando tablas de autenticación...")
    AuthBase.metadata.create_all(bind=engine)
    print("Tablas de autenticación creadas exitosamente!")

if __name__ == "__main__":
    crear_tablas()
