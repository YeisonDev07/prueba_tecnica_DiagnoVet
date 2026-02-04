"""
Modelos de datos de la aplicación.
Define la estructura de los datos que entran y salen de la API.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class VeterinaryReport(BaseModel):
    """
    Modelo que representa un reporte de ultrasonido veterinario.
    Este es el formato JSON que devolverá nuestra API.
    """
    id: str = Field(..., description="ID único del reporte")
    
    # Información extraída del PDF
    patient_name: Optional[str] = Field(None, description="Nombre del paciente (animal)")
    owner_name: Optional[str] = Field(None, description="Nombre del dueño")
    veterinarian_name: Optional[str] = Field(None, description="Nombre del veterinario")
    diagnosis: Optional[str] = Field(None, description="Diagnóstico médico")
    recommendations: Optional[str] = Field(None, description="Recomendaciones")
    
    # Imágenes extraídas
    image_urls: List[str] = Field(default_factory=list, description="URLs de las imágenes en Cloud Storage")
    
    # Metadata
    pdf_filename: str = Field(..., description="Nombre original del PDF")
    upload_date: datetime = Field(default_factory=datetime.utcnow, description="Fecha de carga")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "abc123xyz",
                "patient_name": "Max",
                "owner_name": "Juan Pérez",
                "veterinarian_name": "Dr. García",
                "diagnosis": "Cálculos renales en riñón izquierdo",
                "recommendations": "Dieta especial baja en calcio, control en 2 semanas",
                "image_urls": [
                    "https://storage.googleapis.com/bucket/image1.png",
                    "https://storage.googleapis.com/bucket/image2.png"
                ],
                "pdf_filename": "reporte_ultrasonido_max.pdf",
                "upload_date": "2026-02-04T10:30:00"
            }
        }


class UploadResponse(BaseModel):
    """
    Respuesta que devuelve el endpoint de upload.
    """
    report_id: str = Field(..., description="ID del reporte creado")
    message: str = Field(..., description="Mensaje de confirmación")
    
    class Config:
        json_schema_extra = {
            "example": {
                "report_id": "abc123xyz",
                "message": "Reporte procesado exitosamente"
            }
        }


class ErrorResponse(BaseModel):
    """
    Formato estándar para errores.
    """
    error: str = Field(..., description="Descripción del error")
    detail: Optional[str] = Field(None, description="Detalle adicional del error")
