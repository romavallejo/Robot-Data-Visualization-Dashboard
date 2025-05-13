from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Sensor(Base):
    __tablename__ = "sensores"
    id_sensor = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tipo = Column(String(50), nullable=False)
    descripcion = Column(String(255), nullable=True)
    
    # Establish a relationship to `Lectura`
    lecturas = relationship("Lectura", back_populates="sensor")

class Lectura(Base):
    __tablename__ = "lecturas"
    id_lectura = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_sensor = Column(Integer, ForeignKey("sensores.id_sensor"), nullable=False)
    medicion = Column(Float, nullable=False)
    tiempo = Column(DateTime, nullable=False, server_default=func.now()) 
    
    # Relationship with Sensor
    sensor = relationship("Sensor", back_populates="lecturas")
