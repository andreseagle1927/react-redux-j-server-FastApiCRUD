from pydantic import BaseModel

class ClinicaBase(BaseModel):
    nombre: str
    direccion: str

class ClinicaCreate(ClinicaBase):
    pass

class Clinica(ClinicaBase):
    clinica_id: int

    class Config:
        from_attributes = True
