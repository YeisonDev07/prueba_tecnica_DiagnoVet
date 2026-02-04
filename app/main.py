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

# Inicializar servicios
pdf_processor = PDFProcessor()

# Inicializar Cloud Storage con el nombre del bucket y project_id configurado
storage_service = GCPStorageService(
    bucket_name=settings.gcs_bucket_name,
    project_id=settings.gcp_project_id
)

# Inicializar Firestore
firestore_service = FirestoreService(project_id=settings.gcp_project_id)


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
        
        # FASE 2 (CLOUD): Subir imágenes a Cloud Storage
        image_urls = []
        if storage_service and len(image_paths) > 0:
            print(f"☁️  Subiendo {len(image_paths)} imágenes a Cloud Storage...")
            image_urls = storage_service.upload_multiple_images(image_paths, report_id)
            print(f"✅ Imágenes disponibles en Cloud Storage")
        
        # FASE 2 (FIRESTORE): Guardar metadata en Firestore
        report_data = {
            "id": report_id,
            "pdf_filename": file.filename,
            "patient_name": None,  # TODO: Extraer con Document AI
            "owner_name": None,
            "veterinarian_name": None,
            "diagnosis": None,
            "recommendations": None,
            "image_urls": image_urls,
            "upload_date": datetime.utcnow(),
            "status": "processed"
        }
        
        if firestore_service:
            firestore_service.save_report(report_data)
        
        # TODO FASE 3: Procesar con Document AI para extraer campos específicos
        
        return UploadResponse(
            report_id=report_id,
            message=f"Reporte procesado. {len(image_paths)} imágenes extraídas y {len(image_urls)} subidas a Cloud Storage."
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
        # Consultar Firestore
        if firestore_service:
            report_data = firestore_service.get_report(report_id)
            
            if report_data:
                # Convertir a modelo Pydantic
                return VeterinaryReport(**report_data)
        
        # Si no se encuentra, error 404
        raise HTTPException(status_code=404, detail=f"Reporte '{report_id}' no encontrado")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo reporte: {str(e)}")


@app.get("/reports")
async def list_reports():
    """
    Lista todos los reportes disponibles.
    Útil para debugging y demostración.
    """
    try:
        if firestore_service:
            reports = firestore_service.list_reports()
            return {
                "total_reports": len(reports),
                "reports": reports
            }
        
        return {
            "message": "Firestore no inicializado",
            "total_reports": 0
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listando reportes: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    # Ejecutar el servidor en modo desarrollo
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
