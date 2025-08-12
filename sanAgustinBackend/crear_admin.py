from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models.auth_models import Usuario
from datetime import datetime

# Crear engine y sesión
SQLALCHEMY_DATABASE_URL = "sqlite:///./comunidad.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def crear_admin():
    db = SessionLocal()
    
    # Verificar si ya existe un admin
    admin_existente = db.query(Usuario).filter(Usuario.is_admin == True).first()
    if admin_existente:
        print(f"Ya existe un administrador: {admin_existente.email}")
        return
    
    # Crear usuario administrador
    admin = Usuario(
        email="admin@sanagustin.com",
        nombre="Administrador",
        apellido="San Agustín",
        provider="manual",
        provider_id="admin_001",
        is_active=True,
        is_admin=True,
        created_at=datetime.utcnow()
    )
    
    db.add(admin)
    db.commit()
    db.refresh(admin)
    
    print(f"Administrador creado exitosamente: {admin.email}")
    print("Credenciales de acceso:")
    print(f"Email: {admin.email}")
    print("Nota: Este usuario se creó manualmente y no requiere OAuth")
    
    db.close()

if __name__ == "__main__":
    crear_admin()
