from typing import List
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from app import crud
from app import schemas
from app.db import engine, session
from app.models import Base
from data import DATOS_PRUEBA
import logging
import settings

logging.basicConfig(filename='myapp.log', level=logging.INFO)

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all) 
    logging.info(" Base iniciada.")
    if settings.TESTING:
        alumnos = await crud.consulta_alumnos(db=session())
        if len(alumnos) == 0:
            logging.info(' La tabla está vacía.')
            logging.info(' Ingresando datos de prueba...')
            for alumno in DATOS_PRUEBA:
                cuenta = alumno["cuenta"]
                candidato = {campo:alumno[campo] for campo in alumno if campo != "cuenta"}
                await crud.alta_alumno(db=session(), 
                                 cuenta=cuenta, 
                                 candidato=candidato)
            logging.info(' Datos de prueba ingresados.')
        else:
            logging.info(" Ya existen datos en la tabla.") 


@app.on_event("shutdown")
async def shutdown_event():
    logging.info(" Cerrando la aplicación.")


@app.get("/api/", response_model=List[schemas.SchemaAlumno])
async def vuelca_base():
    alumnos = await crud.consulta_alumnos(db=session())
    return alumnos


@app.get("/api/{cuenta:int}")
async def get_alumno(cuenta, response_model=schemas.SchemaAlumno):
    alumno = await crud.consulta_alumno(db=session(), cuenta=cuenta)
    if alumno:
        return alumno
    else:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")

       
@app.delete("/api/{cuenta:int}")
async def delete_alumno(cuenta):
    alumno = await crud.consulta_alumno(db=session(), cuenta=cuenta)
    if alumno:
        await crud.baja_alumno(db=session(), alumno=alumno)
        return {'message': "OK"}
    else:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")

        
@app.post("/api/{cuenta:int}", response_model=schemas.SchemaAlumno)
async def post_alumno(cuenta, candidato: schemas.SchemaAlumnoIn):
    alumno = await crud.consulta_alumno(db=session(), cuenta=cuenta)
    if alumno:
        raise HTTPException(status_code=409, detail="Recurso existente")
    return await crud.alta_alumno(db=session(), cuenta=cuenta, candidato=candidato)        
        
        
@app.put("/api/{cuenta:int}", response_model=schemas.SchemaAlumno)
async def put_alumno(cuenta, candidato: schemas.SchemaAlumnoIn):
    alumno = await crud.consulta_alumno(db=session(), cuenta=cuenta)
    if alumno:
        await crud.baja_alumno(db=session(), alumno=alumno)
        return await crud.alta_alumno(db=session(), cuenta=cuenta, candidato=candidato)
    else:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")