"""
API Principal de DiagnoVET Challenge.
Endpoints para subir PDFs de reportes veterinarios y consultarlos.
"""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
import uuid
from datetime import datetime

from app.models import VeterinaryReport, UploadResponse, ErrorResponse
from app.config import get_settings
from app.services.pdf_processor import PDFProcessor
from app.services.gcp_storage import GCPStorageService
from app.services.firestore_db import FirestoreService

# Inicializar la aplicación FastAPI
app = FastAPI(
    title="DiagnoVET PDF Processor API",
    description="API para procesar reportes de ultrasonido veterinario",
    version="1.0.0"
)

# Cargar configuración
settings = get_settings()

# Inicializar servicios (solo si no estamos en modo local sin GCP)
# Por ahora los dejamos como None para desarrollo local
pdf_processor = PDFProcessor()
storage_service = None  # GCPStorageService() - activaremos después
firestore_service = None  # FirestoreService() - activaremos después


@app.get("/")
async def root():
    """
    Endpoint de salud (health check).
    Verifica que la API esté funcionando.
    """
    return {
        "status": "online",
        "service": "DiagnoVET PDF Processor",
        "version": "1.0.0",
        "environment": settings.environment
    }


@app.post("/upload-report", response_model=UploadResponse)
async def upload_report(file: UploadFile = File(...)):
    """
    Endpoint para subir un PDF de reporte veterinario.
    
    Flujo:
    1. Recibe el PDF
    2. Lo guarda temporalmente
    3. Extrae texto con Document AI (o OCR local por ahora)
    4. Extrae imágenes del PDF
    5. Sube imágenes a Cloud Storage
    6. Guarda metadata en Firestore
    7. Retorna el ID del reporte
    """
    try:
        # Validar que sea un PDF
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Solo se aceptan archivos PDF")
        
        # Generar ID único para este reporte
        report_id = str(uuid.uuid4())[:8]  # Usamos solo los primeros 8 caracteres
        
        # Guardar PDF temporalmente
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        pdf_path = os.path.join(upload_dir, f"{report_id}_{file.filename}")
        
        # Leer y guardar el archivo
        with open(pdf_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        print(f"✅ PDF guardado en: {pdf_path}")
        
        # FASE 1 (LOCAL): Solo extraer texto básico por ahora
        extracted_text = pdf_processor.extract_text(pdf_path)
        print(f"📄 Texto extraído: {len(extracted_text)} caracteres")
        
        # FASE 1 (LOCAL): Extraer imágenes del PDF
        image_paths = pdf_processor.extract_images(pdf_path, report_id)
        print(f"🖼️  Imágenes extraídas: {len(image_paths)}")
        
        # TODO FASE 2: Subir imágenes a Cloud Storage
        # TODO FASE 2: Procesar con Document AI para extraer campos específicos
        # TODO FASE 2: Guardar en Firestore
        
        # Por ahora, retornamos respuesta básica
        return UploadResponse(
            report_id=report_id,
            message=f"Reporte procesado localmente. {len(image_paths)} imágenes extraídas."
        )
        
    except Exception as e:
        print(f"❌ Error procesando PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error procesando PDF: {str(e)}")


@app.get("/reports/{report_id}", response_model=VeterinaryReport)
async def get_report(report_id: str):
    """
    Obtiene un reporte por su ID.
    
    Consulta Firestore y retorna los datos estructurados con URLs de imágenes.
    """
    try:
        # TODO FASE 2: Consultar Firestore
        # Por ahora retornamos datos de ejemplo
        
        # Simulación de datos
        return VeterinaryReport(
            id=report_id,
            patient_name="Max (ejemplo local)",
            owner_name="Juan Pérez (ejemplo)",
            veterinarian_name="Dr. García (ejemplo)",
            diagnosis="Pendiente de procesamiento con Document AI",
            recommendations="En desarrollo",
            image_urls=[],
            pdf_filename="ejemplo.pdf",
            upload_date=datetime.utcnow()
        )
        
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Reporte no encontrado: {str(e)}")


@app.get("/reports")
async def list_reports():
    """
    Lista todos los reportes disponibles.
    Útil para debugging y demostración.
    """
    # TODO FASE 2: Consultar todos los documentos de Firestore
    return {
        "message": "Endpoint en desarrollo",
        "total_reports": 0
    }


if __name__ == "__main__":
    import uvicorn
    # Ejecutar el servidor en modo desarrollo
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
