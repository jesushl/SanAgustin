from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import sessionmaker, relationship
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta

import logging
logging.basicConfig(level=logging.INFO)

# Importar modelos de autenticación
# from models.auth_models import Usuario, RegistroPendiente, Contacto as ContactoAuth

# Creación de la base y el engine
SQLALCHEMY_DATABASE_URL = "sqlite:///./comunidad.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Creación de la aplicación FastAPI
app = FastAPI(
    title="San Agustín API",
    description="API para la gestión de servicios de la privada San Agustín",
    version="1.0.0"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos SQLAlchemy

class Departamento(Base):
    __tablename__ = "departamentos"
    id = Column(Integer, primary_key=True, index=True)
    numero = Column(String, index=True)
    estacionamientos = relationship("Estacionamiento", back_populates="departamento")
    contacto_id = Column(Integer, ForeignKey("contactos.id"))
    contacto = relationship("Contacto", back_populates="departamentos")
    adeudos = relationship("Adeudo", back_populates="departamento")
    reservas_area_comun = relationship("ReservaAreaComun", back_populates="departamento")  # <--- esta línea

class AreaComun(Base):
    __tablename__ = "areas_comunes"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    descripcion = Column(String)
    ubicacion = Column(String)
    reservas = relationship("ReservaAreaComun", back_populates="area_comun")
    # Relación con el modelo ReservaAreaComun


class Contacto(Base):
    __tablename__ = "contactos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    apellido = Column(String)
    numero_contacto = Column(String)
    correo = Column(String)
    departamentos = relationship("Departamento", back_populates="contacto")

class ReservaAreaComun(Base):
    __tablename__ = "reservas_area_comun"

    id = Column(Integer, primary_key=True, index=True)
    area = Column(Integer, ForeignKey("areas_comunes.id"))
    periodo_inicio = Column(DateTime)
    periodo_fin = Column(DateTime)
    departamento_id = Column(Integer, ForeignKey("departamentos.id"))
    area_comun = relationship("AreaComun", back_populates="reservas")
    departamento = relationship("Departamento", back_populates="reservas_area_comun")

class ContactoResidente(Base):
    __tablename__ = "contactos_residente"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    apellido = Column(String)
    numero_contacto = Column(String)
    correo_electronico = Column(String)

class Estacionamiento(Base):
    __tablename__ = "estacionamientos"
    id = Column(Integer, primary_key=True, index=True)
    numero = Column(String)
    placa = Column(String)
    modelo_auto = Column(String)
    color_auto = Column(String)
    es_visita = Column(Integer, default=0)  # 0: No es visita, 1: Es visita
    departamento_id = Column(Integer, ForeignKey("departamentos.id"))
    departamento = relationship("Departamento", back_populates="estacionamientos")
    reservas_visita = relationship("ReservaVisita", back_populates="estacionamiento")

class ReservaVisita(Base):
    __tablename__ = "reservas_visita"

    id = Column(Integer, primary_key=True, index=True)
    estacionamiento_id = Column(Integer, ForeignKey("estacionamientos.id"))
    placas_visita = Column(String)
    periodo_inicio = Column(DateTime)
    periodo_fin = Column(DateTime)

    estacionamiento = relationship("Estacionamiento", back_populates="reservas_visita")

class Adeudo(Base):
    __tablename__ = "adeudos"
    id = Column(Integer, primary_key=True, index=True)
    departamento_id = Column(Integer, ForeignKey("departamentos.id"))
    monto = Column(Float)
    descripcion = Column(String)
    fecha = Column(DateTime, default=datetime.utcnow)
    departamento = relationship("Departamento", back_populates="adeudos")


# Modelos Pydantic para validación y respuestas

class EstacionamientoResponse(BaseModel):
    numero_estacionamiento: str
    placa: str
    modelo: str
    color: str
    es_visita: bool

    model_config = {
        "from_attributes": True
    }

class ReservaAutomaticaVisita(BaseModel):
    numero_departamento: str
    placas_visita: str
    hora_llegada: datetime
    horas_estancia: int


class ContactoResponse(BaseModel):
    nombre: str
    apellido: str
    numero_contacto: str
    correo: str

    model_config = {
        "from_attributes": True
    }


class ReservaAreaComunBase(BaseModel):
    area: str  # Puede ser "palapa", "roofgarden_a", "roofgarden_b", etc.
    periodo_inicio: datetime
    periodo_fin: datetime
    departamento_id: int

    model_config = {
        "from_attributes": True
    }

class ReservaAreaComunResponse(ReservaAreaComunBase):
    id: int

class ContactoResidenteBase(BaseModel):
    nombre: str
    apellido: str
    numero_contacto: str
    correo_electronico: str

    model_config = {
        "from_attributes": True
    }

class ContactoResidenteResponse(ContactoResidenteBase):
    id: int

class AdeudoResponse(BaseModel):
    id: int
    departamento_id: int
    monto: float
    descripcion: str
    fecha: datetime

    model_config = {
        "from_attributes": True
    }

class AdeudoCreate(BaseModel):
    departamento_id: int
    monto: float
    descripcion: str


# Función para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# Endpoints

@app.get("/estacionamientos/{numero_estacionamiento}", response_model=EstacionamientoResponse)
def obtener_estacionamiento(numero_estacionamiento: str, db: Session = Depends(get_db)):
    logging.info(f'Numero de estacionamiento {numero_estacionamiento}')
    estacionamiento = db.query(Estacionamiento).filter(Estacionamiento.numero == numero_estacionamiento).first()
    if not estacionamiento:
        raise HTTPException(status_code=404, detail="Estacionamiento no encontrado")
    
    
    return {
        "numero_estacionamiento": estacionamiento.numero, 
        "placa": estacionamiento.placa, 
        "modelo": estacionamiento.modelo_auto, 
        "color": estacionamiento.color_auto, 
        "es_visita":  bool(estacionamiento.es_visita)
    }
    

@app.get("/placas/{placa}")
def validar_placa(placa: str, db: Session = Depends(get_db)):
    estacionamiento = db.query(Estacionamiento).filter(Estacionamiento.placa == placa).first()
    
    if not estacionamiento:
        raise HTTPException(status_code=404, detail="Placa no registrada como residente")
    
    return {
        "placa": estacionamiento.placa,
        "numero_estacionamiento": estacionamiento.numero,
        "departamento": estacionamiento.departamento.numero
    }


@app.post("/reservas_visitas/")
def reservar_visita_automatico(datos: ReservaAutomaticaVisita, db: Session = Depends(get_db)):
    # Obtener el departamento por número
    departamento = db.query(Departamento).filter(Departamento.numero == datos.numero_departamento).first()
    if not departamento:
        raise HTTPException(status_code=404, detail="Departamento no encontrado")

    # Calcular el periodo de reserva
    inicio = datos.hora_llegada
    fin = inicio + timedelta(hours=datos.horas_estancia)

    # Obtener estacionamientos de visita
    estacionamientos_visita = db.query(Estacionamiento).filter(Estacionamiento.es_visita == 1).all()

    for est in estacionamientos_visita:
        # Revisar si el estacionamiento está libre en el tiempo solicitado
        reservas_existentes = db.query(ReservaVisita).filter(
            ReservaVisita.estacionamiento_id == est.id,
            ReservaVisita.periodo_fin > inicio,
            ReservaVisita.periodo_inicio < fin
        ).all()

        if not reservas_existentes:
            # Estacionamiento disponible
            nueva_reserva = ReservaVisita(
                estacionamiento_id=est.id,
                placas_visita=datos.placas_visita,
                periodo_inicio=inicio,
                periodo_fin=fin
            )
            db.add(nueva_reserva)
            db.commit()
            db.refresh(nueva_reserva)
            return nueva_reserva

    raise HTTPException(status_code=400, detail="No hay estacionamientos de visita disponibles en este horario.")

@app.post("/reservas_area_comun/", response_model=ReservaAreaComunResponse)
def reservar_area_comun(reserva: ReservaAreaComunBase, db: Session = Depends(get_db)):
    # Verificar que el departamento existe
    departamento = db.query(Departamento).filter(Departamento.id == reserva.departamento_id).first()
    if not departamento:
        raise HTTPException(status_code=404, detail="Departamento no encontrado")
    
    # Buscar el área común por nombre
    area = db.query(AreaComun).filter(AreaComun.nombre == reserva.area).first()
    if not area:
        raise HTTPException(status_code=404, detail="Área común no encontrada")

    # Validar que no se solape con otra reserva
    existe_reserva = db.query(ReservaAreaComun).filter(
        ReservaAreaComun.area == area.id,
        ReservaAreaComun.periodo_inicio < reserva.periodo_fin,
        ReservaAreaComun.periodo_fin > reserva.periodo_inicio
    ).first()

    if existe_reserva:
        raise HTTPException(status_code=400, detail="El área común ya está reservada en ese periodo.")

    # Crear la reserva
    nueva_reserva = ReservaAreaComun(
        area=area.id,
        departamento_id=reserva.departamento_id,
        periodo_inicio=reserva.periodo_inicio,
        periodo_fin=reserva.periodo_fin
    )

    db.add(nueva_reserva)
    db.commit()
    db.refresh(nueva_reserva)

    return nueva_reserva

@app.get("/reservas_area_comun/", response_model=List[ReservaAreaComunResponse])
def obtener_reservas_area_comun(db: Session = Depends(get_db)):
    reservas = db.query(ReservaAreaComun).all()
    return reservas

@app.post("/contactos_residente/", response_model=ContactoResidenteResponse)
def registrar_contacto_residente(contacto: ContactoResidenteResponse, db: Session = Depends(get_db)):
    db.add(contacto)
    db.commit()
    db.refresh(contacto)
    return contacto

@app.get("/contactos_residente/", response_model=List[ContactoResidenteResponse])
def obtener_contactos_residente(db: Session = Depends(get_db)):
    contactos = db.query(ContactoResidente).all()
    return contactos

@app.get("/contactos_residente/{contacto_id}", response_model=ContactoResidenteResponse)
def obtener_contacto_residente(contacto_id: int, db: Session = Depends(get_db)):
    contacto = db.query(ContactoResidente).filter(ContactoResidente.id == contacto_id).first()
    if not contacto:
        raise HTTPException(status_code=404, detail="Contacto no encontrado")
    return contacto

@app.get("/estacionamientos_residentes/{estacionamiento_id}", response_model=EstacionamientoResponse)
def obtener_estacionamiento_residente(estacionamiento_id: int, db: Session = Depends(get_db)):
    estacionamiento = db.query(Estacionamiento).filter(Estacionamiento.id == estacionamiento_id).first()
    if not estacionamiento:
        raise HTTPException(status_code=404, detail="Estacionamiento no encontrado")
    return estacionamiento

@app.get("/placas_residentes/{placa}", response_model=EstacionamientoResponse)
def obtener_lugar_por_placa(placa: str, db: Session = Depends(get_db)):
    estacionamiento = db.query(Estacionamiento).filter(Estacionamiento.placas == placa).first()
    if not estacionamiento:
        raise HTTPException(status_code=404, detail="Placa no registrada como residente")
    return estacionamiento


@app.get("/adeudos/", response_model=list[AdeudoResponse])
def listar_todos_adeudos(db: Session = Depends(get_db)):
    return db.query(Adeudo).all()

@app.get("/adeudos/{departamento_id}", response_model=list[AdeudoResponse])
def listar_adeudos_departamento(departamento_id: int, db: Session = Depends(get_db)):
    adeudos = db.query(Adeudo).filter(Adeudo.departamento_id == departamento_id).all()
    if not adeudos:
        raise HTTPException(status_code=404, detail="No se encontraron adeudos para este departamento")
    return adeudos

@app.post("/adeudos/", response_model=AdeudoResponse)
def crear_adeudo(adeudo: AdeudoCreate, db: Session = Depends(get_db)):
    nuevo_adeudo = Adeudo(**adeudo.dict())
    db.add(nuevo_adeudo)
    db.commit()
    db.refresh(nuevo_adeudo)
    return nuevo_adeudo


@app.post("/estacionamiento_qr/")
def generar_qr_estacionamiento(estacionamiento: EstacionamientoResponse, db: Session = Depends(get_db)):
    # Aquí iría la lógica para generar el QR
    return {"message": "QR generado", "estacionamiento": estacionamiento}

@app.post("/vehiculo_qr_info/")
def leer_qr_vehiculo(qr_data: str, db: Session = Depends(get_db)):
    # Aquí iría la lógica para leer el QR y obtener la información del vehículo
    return {"message": "QR leído", "data": qr_data}

# Importar y incluir las rutas de autenticación
# from api.auth_routes import router as auth_router
# app.include_router(auth_router)

# Configurar OAuth
# from core.oauth_config import oauth
# oauth.init_app(app)