from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Sensor, Lectura
from crud import create_sensor,get_sensor,get_sensors,create_lectura, get_lecturas, get_mediciones_by_sensor, get_last_medicion_by_sensor

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"] #cambiar

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/sensors/mediciones/")
async def get_mediciones(db: Session = Depends(get_db)):
    mediciones = [] 
    for i in range(8):
        sensor_mediciones = get_mediciones_by_sensor(db, i+1)
        if sensor_mediciones:
            mediciones.append(sensor_mediciones)
        else:
            mediciones.append([])  

    try:
        mediciones_data = [[m[0] for m in sensor] if sensor else [] for sensor in mediciones]
        tiempo_data = [m[1] for m in mediciones[5]] if mediciones[5] else []
    except IndexError:
        raise HTTPException(status_code=500, detail="Error procesando las mediciones")

    return {
        "mediciones": mediciones_data,
        "tiempo": tiempo_data
    }

