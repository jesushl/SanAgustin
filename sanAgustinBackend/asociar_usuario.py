from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

# Crear engine y sesión
SQLALCHEMY_DATABASE_URL = "sqlite:///./comunidad.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelos SQLAlchemy
class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    provider = Column(String, nullable=False)
    provider_id = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

class Departamento(Base):
    __tablename__ = "departamentos"
    id = Column(Integer, primary_key=True, index=True)
    numero = Column(String, index=True, unique=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)

def asociar_usuario():
    db = SessionLocal()
    
    try:
        # Crear un usuario de prueba
        usuario = Usuario(
            email="residente@test.com",
            nombre="Juan",
            apellido="Pérez",
            provider="google",
            provider_id="123456789",
            is_active=True,
            is_admin=False
        )
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        
        # Asociar el departamento 01 al usuario
        departamento = db.query(Departamento).filter(Departamento.numero == "01").first()
        if departamento:
            departamento.usuario_id = usuario.id
            db.commit()
            print(f"Usuario {usuario.email} asociado al departamento {departamento.numero}")
        else:
            print("No se encontró el departamento 01")
        
        # Crear un usuario admin
        admin = Usuario(
            email="admin@test.com",
            nombre="Admin",
            apellido="Sistema",
            provider="google",
            provider_id="987654321",
            is_active=True,
            is_admin=True
        )
        db.add(admin)
        db.commit()
        
        print("Usuarios creados exitosamente!")
        print(f"- Residente: {usuario.email} (ID: {usuario.id})")
        print(f"- Admin: {admin.email} (ID: {admin.id})")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    asociar_usuario()
