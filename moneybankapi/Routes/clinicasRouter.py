from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from Schemas.clinicasSchemas import ClinicaBase
from Config.database import SessionLocal
from Models.clinicasModel import ClinicaModel

router = APIRouter()
# Rutas para la entidad "Clinica"
@router.get("/clinicas", tags=["Clinicas"])
async def get_all_clinicas():
    try:
        clinicas = SessionLocal().query(ClinicaModel).all()
        return clinicas
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "Internal Server Error", "detail": str(e)})

@router.get("/clinicas/{id}", tags=["Clinicas"])
async def get_clinica_by_id(id: int):
    try:
        clinica = SessionLocal().query(ClinicaModel).filter(ClinicaModel.clinica_id == id).first()
        if clinica is None:
            raise HTTPException(status_code=404, detail="Clinica not found")
        return clinica
    
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "Internal Server Error", "detail": str(e)})

@router.post("/clinicas", tags=["Clinicas"])
async def create_clinica(clinica: ClinicaBase):
    session = SessionLocal()
    
    try:
        new_clinica = ClinicaModel(
            nombre=clinica.nombre,
            direccion=clinica.direccion
        )
        
        session.add(new_clinica)
        session.commit()
        
        session.refresh(new_clinica)
        
        return new_clinica
    
    except HTTPException as http_exc:
        session.rollback()
        raise http_exc
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "Internal Server Error", "detail": str(e)})
    finally:
        session.close()

@router.put("/clinicas/{id}", tags=["Clinicas"])
async def update_clinica(id: int, clinica: ClinicaBase):
    session = SessionLocal()

    try:
        existing_clinica = session.query(ClinicaModel).filter(ClinicaModel.clinica_id == id).first()

        if existing_clinica is None:
            raise HTTPException(status_code=404, detail="Clinica not found")

        existing_clinica.nombre = clinica.nombre
        existing_clinica.direccion = clinica.direccion

        session.commit()

        session.refresh(existing_clinica)

        return existing_clinica
    
    except HTTPException as http_exc:
        session.rollback()
        raise http_exc
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "Internal Server Error", "detail": str(e)})
    finally:
        session.close()

@router.delete("/clinicas/{id}", tags=["Clinicas"])
async def delete_clinica(id: int):
    session = SessionLocal()

    try:
        existing_clinica = session.query(ClinicaModel).filter(ClinicaModel.clinica_id == id).first()

        if existing_clinica is None:
            raise HTTPException(status_code=404, detail="Clinica not found")

        session.delete(existing_clinica)

        session.commit()

        return {"message": "Clinica deleted"}
    
    except HTTPException as http_exc:
        session.rollback()
        raise http_exc
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "Internal Server Error", "detail": str(e)})
    finally:
        session.close()