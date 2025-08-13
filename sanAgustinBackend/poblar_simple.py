from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from datetime import datetime, timedelta

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

class AreaComun(Base):
    __tablename__ = "areas_comunes"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    descripcion = Column(String)
    ubicacion = Column(String)
    capacidad = Column(Integer, default=1)

class LugarVisita(Base):
    __tablename__ = "lugares_visita"
    id = Column(Integer, primary_key=True, index=True)
    numero = Column(String, unique=True)
    descripcion = Column(String)
    capacidad = Column(Integer, default=1)

class Estacionamiento(Base):
    __tablename__ = "estacionamientos"
    id = Column(Integer, primary_key=True, index=True)
    numero = Column(String, unique=True)
    placa = Column(String)
    modelo_auto = Column(String)
    color_auto = Column(String)
    es_visita = Column(Boolean, default=False)
    departamento_id = Column(Integer, ForeignKey("departamentos.id"))

class Adeudo(Base):
    __tablename__ = "adeudos"
    id = Column(Integer, primary_key=True, index=True)
    departamento_id = Column(Integer, ForeignKey("departamentos.id"))
    monto = Column(Float)
    descripcion = Column(String)
    fecha_vencimiento = Column(DateTime)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    pagado = Column(Boolean, default=False)

def poblar_base_datos():
    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Crear áreas comunes
        areas_comunes = [
            AreaComun(
                nombre="Palapa",
                descripcion="Área de recreación con palapa y asadores",
                ubicacion="Planta baja",
                capacidad=20
            ),
            AreaComun(
                nombre="Roof Garden A",
                descripcion="Terraza con vista panorámica",
                ubicacion="Azotea Torre A",
                capacidad=15
            ),
            AreaComun(
                nombre="Roof Garden B",
                descripcion="Terraza con vista panorámica",
                ubicacion="Azotea Torre B",
                capacidad=15
            ),
            AreaComun(
                nombre="Sala de Eventos",
                descripcion="Sala para eventos sociales",
                ubicacion="Planta baja",
                capacidad=50
            ),
            AreaComun(
                nombre="Gimnasio",
                descripcion="Área de ejercicio con equipos",
                ubicacion="Planta baja",
                capacidad=10
            )
        ]
        
        for area in areas_comunes:
            db.add(area)
        
        # Crear lugares de visita
        lugares_visita = [
            LugarVisita(
                numero="V1",
                descripcion="Lugar de visita 1",
                capacidad=1
            ),
            LugarVisita(
                numero="V2",
                descripcion="Lugar de visita 2",
                capacidad=1
            ),
            LugarVisita(
                numero="V3",
                descripcion="Lugar de visita 3",
                capacidad=1
            ),
            LugarVisita(
                numero="V4",
                descripcion="Lugar de visita 4",
                capacidad=1
            ),
            LugarVisita(
                numero="V5",
                descripcion="Lugar de visita 5",
                capacidad=1
            )
        ]
        
        for lugar in lugares_visita:
            db.add(lugar)
        
        # Crear departamentos de ejemplo
        departamentos = []
        for i in range(1, 21):  # 20 departamentos
            depto = Departamento(numero=f"{i:02d}")
            departamentos.append(depto)
            db.add(depto)
        
        # Crear estacionamientos para algunos departamentos
        estacionamientos = [
            Estacionamiento(
                numero="E01",
                placa="ABC123",
                modelo_auto="Toyota Corolla",
                color_auto="Blanco",
                es_visita=False,
                departamento_id=1
            ),
            Estacionamiento(
                numero="E02",
                placa="DEF456",
                modelo_auto="Honda Civic",
                color_auto="Negro",
                es_visita=False,
                departamento_id=2
            ),
            Estacionamiento(
                numero="E03",
                placa="GHI789",
                modelo_auto="Nissan Sentra",
                color_auto="Gris",
                es_visita=False,
                departamento_id=3
            ),
            # Estacionamientos de visita
            Estacionamiento(
                numero="V01",
                es_visita=True,
                departamento_id=None
            ),
            Estacionamiento(
                numero="V02",
                es_visita=True,
                departamento_id=None
            ),
            Estacionamiento(
                numero="V03",
                es_visita=True,
                departamento_id=None
            )
        ]
        
        for est in estacionamientos:
            db.add(est)
        
        # Crear algunos adeudos de ejemplo
        adeudos = [
            Adeudo(
                departamento_id=1,
                monto=1500.00,
                descripcion="Mantenimiento mensual",
                fecha_vencimiento=datetime.now() + timedelta(days=15),
                pagado=False
            ),
            Adeudo(
                departamento_id=5,
                monto=2300.00,
                descripcion="Mantenimiento mensual",
                fecha_vencimiento=datetime.now() + timedelta(days=5),
                pagado=False
            ),
            Adeudo(
                departamento_id=10,
                monto=800.00,
                descripcion="Mantenimiento mensual",
                fecha_vencimiento=datetime.now() - timedelta(days=10),
                pagado=False
            )
        ]
        
        for adeudo in adeudos:
            db.add(adeudo)
        
        # Commit todos los cambios
        db.commit()
        
        print("Base de datos poblada exitosamente!")
        print(f"- {len(areas_comunes)} áreas comunes creadas")
        print(f"- {len(lugares_visita)} lugares de visita creados")
        print(f"- {len(departamentos)} departamentos creados")
        print(f"- {len(estacionamientos)} estacionamientos creados")
        print(f"- {len(adeudos)} adeudos de ejemplo creados")
        
    except Exception as e:
        print(f"Error al poblar la base de datos: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    poblar_base_datos()
