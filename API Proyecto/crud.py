from sqlalchemy.orm import Session
from models import Sensor, Lectura

# CRUD for Sensor
def create_sensor(db: Session, tipo: str, descripcion: str = None):
    sensor = Sensor(tipo=tipo, descripcion=descripcion)
    db.add(sensor)
    db.commit()
    db.refresh(sensor)
    return sensor

def get_sensor(db: Session, sensor_id: int):
    return db.query(Sensor).filter(Sensor.id_sensor == sensor_id).first()

def get_sensors(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Sensor).offset(skip).limit(limit).all()

def create_lectura(db: Session, id_sensor: int, medicion: float, tiempo=None):
    lectura = Lectura(id_sensor=id_sensor, medicion=medicion, tiempo=tiempo)
    db.add(lectura)
    db.commit()
    db.refresh(lectura)
    return lectura

def get_lecturas(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Lectura).offset(skip).limit(limit).all()

#los crud que uso
def get_mediciones_by_sensor(db: Session, sensor_id: int):
    return db.query(Lectura.medicion, Lectura.tiempo).filter(Lectura.id_sensor == sensor_id).all()

def get_last_medicion_by_sensor(db: Session, sensor_id: int):
    return (
        db.query(Lectura).filter(Lectura.id_sensor == sensor_id).order_by(Lectura.tiempo.desc()).first()
    )