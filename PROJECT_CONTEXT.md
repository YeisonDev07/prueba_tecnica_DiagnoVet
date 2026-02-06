# Context Completo del Proyecto DiagnoVET Backend Challenge

## 🎯 Objetivo del Proyecto

Construir una API REST que procese reportes veterinarios en PDF (ultrasonido, radiografías) y extraiga automáticamente:

- Imágenes médicas embebidas (radiografías, ultrasonidos)
- Información estructurada: nombre del paciente, propietario, veterinario, diagnóstico, recomendaciones
- Todo almacenado en Google Cloud Platform con arquitectura serverless

**Challenge técnico de diagnoVET:** Demostrar habilidad para aprender tecnologías GCP desconocidas y construir solución funcional en 72 horas.

## 👤 Contexto del Desarrollador

**Nombre:** Yeison  
**Situación:** Recibió oferta de empleo en LinkedIn de startup veterinaria diagnoVET para posición Backend Engineer

**Nivel técnico al inicio:**

- ✅ Experiencia con Python, FastAPI, APIs REST
- ❌ CERO experiencia con Google Cloud Platform
- ❌ Nunca usó Cloud Storage, Firestore, Document AI
- ❌ No conocía conceptos de cloud computing serverless

**Enfoque elegido:**

- Comunicación honesta con recruiter sobre gaps de conocimiento
- Aprendizaje incremental paso a paso con explicaciones detalladas
- Documentar cada decisión técnica para poder explicarla en video demo
- **NO** entregar algo muy elaborado, sino algo que entienda 100% para explicarlo confiadamente

**Filosofía:**

> "Cada cosa que se haga debe ser capaz de identificarla y aprenderla para que cuando haga el video explicativo lo pueda hacer de la mejor manera sin adivinar cosas"

## 📊 Estado Actual del Proyecto

**Versión:** 0.2.0  
**Fases completadas:** 1 y 2 de 6  
**Tiempo invertido:** ~3 horas de desarrollo activo  
**Código funcional:** 100% operativo para procesamiento de PDFs, extracción de imágenes, almacenamiento en Cloud Storage, persistencia en Firestore  
**Próximo paso:** Integración de Document AI para OCR inteligente (Fase 3)

### ✅ Fase 1: Procesamiento Local + Cloud Storage (COMPLETADA)

**Duración:** ~2 horas

**Objetivos logrados:**

1. Configuración de entorno Python con venv
2. Instalación de dependencias (FastAPI, PyPDF2, google-cloud-storage)
3. Implementación de API REST con FastAPI
4. Extracción de texto e imágenes de PDFs usando PyPDF2
5. Creación de bucket en Cloud Storage
6. Servicio de subida de imágenes a GCS con URLs públicas
7. Application Default Credentials configurado (sin JSON keys)

**Archivos creados:**

- `app/main.py` - API principal con endpoints
- `app/services/pdf_processor.py` - Lógica de extracción de PDFs
- `app/services/gcp_storage.py` - Cliente de Cloud Storage
- `app/models.py` - Modelos Pydantic para validación
- `app/config.py` - Configuración con variables de entorno
- `requirements.txt` - Dependencias fijadas
- `.env` - Variables de entorno
- `.gitignore` - Exclusión de archivos sensibles

**Testing realizado:**

- PDF de prueba: "Estudio Radiográfico Ramón.pdf"
- Resultado: 13 imágenes extraídas exitosamente
- Imágenes subidas a: `gs://diagnovet-reports-images/reports/62b7d119/`
- URLs públicas generadas y accesibles

**Comandos GCP ejecutados:**

```bash
gcloud auth application-default login
gcloud config set project project-630f5850-5bf8-4280-808
gcloud services enable storage.googleapis.com
gsutil mb -p project-630f5850-5bf8-4280-808 -l us-central1 gs://diagnovet-reports-images
gsutil iam ch allUsers:objectViewer gs://diagnovet-reports-images
```

**Git commit:**

```
commit 5a71183
feat: implementar extracción de PDFs y subida a Cloud Storage

Sistema completo de procesamiento local funcionando:
- Extracción de imágenes con PyPDF2 (13 imágenes de PDF test)
- Subida a Cloud Storage con URLs públicas
- Endpoint POST /upload-report operativo
```

### ✅ Fase 2: Integración de Firestore (COMPLETADA)

**Duración:** ~1 hora

**Objetivos logrados:**

1. Habilitación de Firestore API en GCP
2. Creación de base de datos Firestore (Native mode, us-central1)
3. Implementación de FirestoreService con CRUD completo
4. Guardar metadata de reportes en colección "reports"
5. Endpoint GET /reports/{id} consultando Firestore
6. Endpoint GET /reports listando todos los reportes
7. Estructura de documento con URLs de imágenes

**Archivos creados/modificados:**

- `app/services/firestore_db.py` - Servicio completo de Firestore
- `app/main.py` - Integración de FirestoreService en endpoints

**Estructura de documento en Firestore:**

```json
{
  "id": "62b7d119",
  "pdf_filename": "Estudio Radiográfico Ramón.pdf",
  "patient_name": null,
  "owner_name": null,
  "veterinarian_name": null,
  "diagnosis": null,
  "recommendations": null,
  "image_urls": [
    "https://storage.googleapis.com/diagnovet-reports-images/reports/62b7d119/62b7d119_image_2.png",
    "https://storage.googleapis.com/diagnovet-reports-images/reports/62b7d119/62b7d119_image_3.jpg"
  ],
  "upload_date": "2026-02-04T20:15:30.123456",
  "status": "processed"
}
```

**Testing en Postman:**

- POST /upload-report → Response: `{"report_id": "62b7d119", "message": "Reporte procesado. 13 imágenes extraídas y 13 subidas a Cloud Storage."}`
- GET /reports/62b7d119 → Retorna documento completo con metadata
- GET /reports → Lista todos los reportes con total_reports

**Comandos GCP ejecutados:**

```bash
gcloud services enable firestore.googleapis.com
gcloud firestore databases create --location=us-central1
gcloud firestore databases list
```

**Git commit:**

```
commit 1f4f53f
feat: integrar Firestore para persistencia de metadata

Sistema completo de base de datos funcionando:
- Integración con Firestore Native mode
- Guardar metadata en colección 'reports'
- GET /reports/{id} con datos reales desde Firestore
- GET /reports lista todos los reportes
- URLs de imágenes almacenadas en Firestore
```

### ⏳ Fase 3: Document AI para OCR Inteligente (PENDIENTE - PRÓXIMO)

**Tiempo estimado:** 30-45 minutos  
**Complejidad:** Media

**Objetivos:**

1. Habilitar Document AI API
2. Crear procesador de documentos (Form Parser o Custom Extractor)
3. Implementar `extract_fields_with_document_ai()` en `pdf_processor.py`
4. Extraer campos: patient_name, owner_name, veterinarian_name, diagnosis, recommendations
5. Actualizar documentos de Firestore con campos extraídos
6. Testing con PDFs reales de diagnoVET

**Tareas específicas:**

```bash
# 1. Habilitar API
gcloud services enable documentai.googleapis.com

# 2. Crear procesador via consola
# https://console.cloud.google.com/ai/document-ai?project=project-630f5850-5bf8-4280-808
# Tipo: Form Parser
# Región: us o eu
```

**Código a implementar en `pdf_processor.py`:**

```python
from google.cloud import documentai_v1 as documentai

def extract_fields_with_document_ai(self, pdf_path: str) -> Dict[str, Optional[str]]:
    """Extrae campos específicos usando Document AI."""
    client = documentai.DocumentProcessorServiceClient()

    # Leer PDF
    with open(pdf_path, "rb") as pdf_file:
        pdf_content = pdf_file.read()

    # Configurar request
    request = documentai.ProcessRequest(
        name=f"projects/{PROJECT_ID}/locations/us/processors/{PROCESSOR_ID}",
        raw_document=documentai.RawDocument(
            content=pdf_content,
            mime_type="application/pdf"
        )
    )

    # Procesar
    result = client.process_document(request=request)
    document = result.document

    # Extraer campos (lógica custom según estructura del PDF)
    fields = {
        "patient_name": None,
        "owner_name": None,
        "veterinarian_name": None,
        "diagnosis": None,
        "recommendations": None
    }

    # Parsear entities o form_fields según tipo de procesador
    for entity in document.entities:
        if entity.type_ == "patient":
            fields["patient_name"] = entity.mention_text
        elif entity.type_ == "veterinarian":
            fields["veterinarian_name"] = entity.mention_text
        # etc...

    return fields
```

**Modificación en `main.py`:**

```python
# En POST /upload-report, después de extraer imágenes
extracted_fields = pdf_processor.extract_fields_with_document_ai(pdf_path)

report_data = {
    "id": report_id,
    "pdf_filename": file.filename,
    **extracted_fields,  # patient_name, owner_name, etc.
    "image_urls": image_urls,
    "upload_date": datetime.now().isoformat(),
    "status": "processed"
}
```

**Verificación:**

- Subir PDF con datos médicos reales
- GET /reports/{id} debe retornar campos NO null
- Validar precisión de nombres extraídos vs PDF original

### ⏳ Fase 4: Deploy a Cloud Run (PENDIENTE)

**Tiempo estimado:** 20-30 minutos  
**Complejidad:** Baja

**Tareas:**

```bash
# 1. Build imagen Docker
gcloud builds submit --tag gcr.io/project-630f5850-5bf8-4280-808/diagnovet-api

# 2. Deploy a Cloud Run
gcloud run deploy diagnovet-api \
  --image gcr.io/project-630f5850-5bf8-4280-808/diagnovet-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GCP_PROJECT_ID=project-630f5850-5bf8-4280-808,GCS_BUCKET_NAME=diagnovet-reports-images

# 3. Obtener URL pública
gcloud run services describe diagnovet-api --region us-central1 --format='value(status.url)'
```

**Testing en producción:**

- POST https://{cloud-run-url}/upload-report con PDF
- Verificar que funciona igual que local

### ⏳ Fase 5: Testing Automatizado (OPCIONAL)

**Tiempo estimado:** 1-2 horas  
**Complejidad:** Media-Alta

### ⏳ Fase 6: Video Demo y Entrega (PENDIENTE)

**Tiempo estimado:** 45-60 minutos  
**Complejidad:** Baja

**Contenido del video (5 minutos):**

1. Introducción (30 seg)
   - Presentación personal
   - Explicación del challenge recibido

2. Arquitectura del sistema (1 min)
   - Diagrama visual de flujo
   - Explicación de cada componente GCP

3. Decisiones técnicas (1.5 min)
   - Por qué FastAPI sobre Flask/Django
   - Por qué Firestore sobre Cloud SQL
   - Por qué PyPDF2 inicialmente y luego Document AI
   - Por qué Application Default Credentials

4. Demo en vivo (2 min)
   - Postman: POST /upload-report con PDF real
   - Mostrar Cloud Storage con imágenes
   - Mostrar Firestore con metadata
   - GET /reports/{id} con datos completos extraídos

5. Código relevante (30 seg)
   - `pdf_processor.py` - Extracción de imágenes
   - `firestore_db.py` - Persistencia de datos
   - `main.py` - Orquestación de servicios

6. Cierre (30 seg)
   - Aprendizajes clave de GCP
   - Próximos pasos si tuviera más tiempo

## 🏗️ Arquitectura Técnica Detallada

### Stack Tecnológico

#### Backend Framework

**FastAPI 0.115.0**

- **Rol:** Framework web principal para API REST
- **Responsabilidades:**
  - Definir endpoints y rutas HTTP
  - Validación automática de requests con Pydantic
  - Generación de documentación OpenAPI
  - Manejo de archivos multipart (PDFs)
- **Por qué se eligió:**
  - Soporte nativo de async/await para operaciones I/O
  - Validación de tipos automática (menos bugs)
  - Documentación interactiva sin configuración extra
  - Performance superior a Flask (~3x más rápido en benchmarks)
- **Dónde se usa:** `app/main.py` - Define los 3 endpoints

**Uvicorn 0.32.0**

- **Rol:** Servidor ASGI para ejecutar FastAPI
- **Responsabilidades:**
  - Servir la aplicación FastAPI
  - Recarga automática en desarrollo (--reload)
  - Gestión de conexiones HTTP
- **Por qué se eligió:**
  - Requerido por FastAPI (no funciona con WSGI)
  - Excelente performance con async
- **Comando:** `python -m uvicorn app.main:app --reload`

#### Procesamiento de PDFs

**PyPDF2 3.0.1**

- **Rol:** Extracción de contenido de archivos PDF
- **Responsabilidades:**
  - Leer texto completo del PDF
  - Extraer imágenes embebidas (radiografías, ultrasonidos)
  - Identificar formato de imágenes (JPEG, PNG)
- **Por qué se eligió:**
  - Sin dependencias externas pesadas (no requiere poppler, tesseract)
  - Funciona offline (no requiere APIs externas)
  - Suficiente para extraer imágenes médicas
  - SIN COSTOS durante desarrollo (Document AI cobra $1.50/1000 páginas)
- **Dónde se usa:** `app/services/pdf_processor.py`
- **Limitaciones conocidas:**
  - No hace OCR de texto en imágenes (para eso se usará Document AI)
  - Algunos warnings "not enough image data" en PDFs complejos (aceptable)

**Pillow 10.4.0**

- **Rol:** Manipulación de imágenes
- **Responsabilidades:**
  - Guardar bytes de imágenes como archivos .jpg/.png
  - Conversión de formatos si es necesario
- **Por qué se eligió:**
  - Requerido por PyPDF2 para procesamiento de imágenes
  - Standard de facto en Python para imaging
- **Dónde se usa:** Usado internamente por PyPDF2

#### Google Cloud Platform

**google-cloud-storage 2.18.2**

- **Rol:** Cliente de Cloud Storage para almacenar imágenes
- **Responsabilidades:**
  - Subir imágenes extraídas a bucket GCS
  - Generar URLs públicas de imágenes
  - Organizar imágenes por report_id
- **Configuración GCP:**
  - Bucket: `diagnovet-reports-images`
  - Región: `us-central1` (baja latencia, costos moderados)
  - Permisos: `allUsers:objectViewer` (lectura pública)
  - Access control: Uniform bucket-level access
- **Patrón de rutas:** `reports/{report_id}/{image_name}.jpg`
- **Por qué se eligió Cloud Storage:**
  - Almacenar imágenes en Firestore es prohibitivo (límite 1MB por documento)
  - URLs directas para acceso HTTP sin pasar por backend
  - CDN integration automática (opcional)
  - Costo: $0.020/GB/mes (muy económico)
- **Dónde se usa:** `app/services/gcp_storage.py`

**google-cloud-firestore 2.19.0**

- **Rol:** Base de datos NoSQL para metadata de reportes
- **Responsabilidades:**
  - Guardar información de cada reporte procesado
  - Almacenar referencias (URLs) a imágenes en Cloud Storage
  - Proveer consultas rápidas por report_id
  - Listar todos los reportes
- **Configuración GCP:**
  - Database ID: `(default)`
  - Modo: Native (no Datastore mode)
  - Región: `us-central1`
  - Edición: Standard
  - Security rules: Production mode (solo acceso autenticado via ADC)
- **Colección:** `reports`
- **Esquema de documento:**
  ```json
  {
    "id": "string (UUID)",
    "pdf_filename": "string",
    "patient_name": "string | null",
    "owner_name": "string | null",
    "veterinarian_name": "string | null",
    "diagnosis": "string | null",
    "recommendations": "string | null",
    "image_urls": ["array of strings"],
    "upload_date": "string (ISO 8601)",
    "status": "processed | error"
  }
  ```
- **Por qué se eligió Firestore sobre Cloud SQL:**
  - Schema-less: No requiere migraciones SQL
  - Datos semi-estructurados: PDFs tienen campos variables
  - Setup rápido: 1 comando vs configurar instancia SQL, VPC, etc.
  - Escalabilidad automática sin provisioning
  - Costo por uso: $0.18/GB almacenado (MVP muy económico)
- **Dónde se usa:** `app/services/firestore_db.py`

**google-cloud-documentai 2.30.0**

- **Rol:** OCR inteligente con machine learning (PENDIENTE USO)
- **Responsabilidades futuras:**
  - Extraer texto de PDFs con alta precisión
  - Identificar entidades: paciente, veterinario, diagnóstico
  - Clasificar campos según tipo de documento médico
- **Configuración GCP (pendiente):**
  - Procesador: Form Parser o Custom Document Extractor
  - Región: us o eu
  - Entrenamiento: Sin entrenamiento custom inicialmente
- **Por qué se usará:**
  - OCR superior a PyPDF2 para texto en imágenes
  - Machine learning preentrenado para documentos médicos
  - Extracción de entidades específicas (nombres, diagnósticos)
- **Costo:** $1.50/1000 páginas procesadas
- **Dónde se usará:** `app/services/pdf_processor.py` - método `extract_fields_with_document_ai()`

#### Validación y Configuración

**Pydantic 2.8.2**

- **Rol:** Validación de datos y serialización
- **Responsabilidades:**
  - Definir modelos de datos tipados
  - Validar requests automáticamente
  - Serializar responses a JSON
- **Modelos definidos:**
  - `VeterinaryReport`: Modelo completo de reporte con todos los campos
  - `UploadResponse`: Response de POST /upload-report
  - `ErrorResponse`: Response de errores HTTP
- **Por qué se eligió:**
  - Integración nativa con FastAPI
  - Type hints mejoran DX y previenen bugs
  - Validación en runtime sin código extra
- **Dónde se usa:** `app/models.py`
- **Nota:** Versión fijada en 2.8.2 para evitar compilación de Rust (pydantic-core 2.23.4 requería Rust toolchain)

**pydantic-settings 2.3.4**

- **Rol:** Gestión de configuración desde variables de entorno
- **Responsabilidades:**
  - Cargar variables desde archivo `.env`
  - Validar configuración al inicio
  - Proveer singleton de configuración
- **Variables gestionadas:**
  - `GCP_PROJECT_ID`: ID del proyecto en GCP
  - `GCS_BUCKET_NAME`: Nombre del bucket de Cloud Storage
  - `ENVIRONMENT`: development | production
- **Dónde se usa:** `app/config.py`
- **Patrón usado:** `@lru_cache` en `get_settings()` para singleton

#### Utilidades

**python-multipart 0.0.12**

- **Rol:** Parseo de requests multipart/form-data
- **Responsabilidades:**
  - Recibir archivos PDF en POST /upload-report
  - Procesar FormData con múltiples campos
- **Por qué se eligió:**
  - Requerido por FastAPI para `UploadFile`
  - Standard de facto en Python web frameworks

### Autenticación GCP

**Application Default Credentials (ADC)**

- **Qué es:** Sistema de autenticación de GCP que busca credenciales automáticamente
- **Cómo funciona:**
  - En local: Usa credenciales de `gcloud auth application-default login`
  - En Cloud Run: Usa service account del servicio automáticamente
- **Por qué se usa:**
  - ✅ Más seguro que archivos JSON de service accounts
  - ✅ Sin riesgo de exponer credenciales en Git
  - ✅ Mismo código funciona en local y producción
  - ✅ Rotación automática de tokens por Google
  - ✅ Recomendado oficialmente por Google Cloud
- **Configuración:**
  ```bash
  gcloud auth application-default login
  ```
- **Dónde se aplica:**
  - `storage.Client()` en `gcp_storage.py`
  - `firestore.Client()` en `firestore_db.py`
  - `documentai.DocumentProcessorServiceClient()` (futuro)

### Flujo de Datos Completo

```
1. Usuario sube PDF
   ↓
2. FastAPI recibe file en POST /upload-report
   ↓
3. PDFProcessor.extract_images(pdf_path)
   - Lee PDF con PyPDF2
   - Extrae imágenes embebidas
   - Guarda temporalmente en extracted_images/
   ↓
4. GCPStorageService.upload_multiple_images(image_paths, report_id)
   - Por cada imagen:
     - Sube a gs://diagnovet-reports-images/reports/{report_id}/{image_name}
     - Genera URL pública: https://storage.googleapis.com/...
   - Retorna array de URLs
   ↓
5. PDFProcessor.extract_fields_with_document_ai(pdf_path) [PENDIENTE]
   - Envía PDF a Document AI
   - Recibe entidades extraídas
   - Retorna dict con patient_name, diagnosis, etc.
   ↓
6. FirestoreService.save_report(report_data)
   - Crea documento en colección "reports"
   - Guarda: id, pdf_filename, image_urls[], campos extraídos, upload_date
   ↓
7. FastAPI retorna response
   {"report_id": "abc123", "message": "Reporte procesado. X imágenes..."}
   ↓
8. Usuario consulta GET /reports/{id}
   ↓
9. FirestoreService.get_report(report_id)
   - Query a Firestore por document ID
   - Retorna documento completo con todas las URLs
   ↓
10. FastAPI retorna VeterinaryReport JSON
    {
      "id": "abc123",
      "image_urls": ["https://...", "https://..."],
      "patient_name": "Ramón",
      ...
    }
```

## 🔐 Configuración de Seguridad

### Implementado ✅

1. **Application Default Credentials**
   - Sin archivos JSON de service accounts
   - Credenciales manejadas por gcloud CLI
   - Rotación automática de tokens

2. **Variables de entorno**
   - Información sensible en `.env` (excluido de Git)
   - `.env.example` con template (sin valores reales)
   - Validación con pydantic-settings

3. **Cloud Storage IAM**
   - Bucket público solo para lectura (objectViewer)
   - Sin permisos de escritura pública
   - Uploads solo via backend autenticado

4. **Firestore Security Rules**
   - Modo producción (no test mode)
   - Acceso solo via backend con ADC
   - Sin acceso directo desde clientes

5. **.gitignore robusto**
   - Excluye: venv/, .env, uploads/, extracted_images/, credentials/
   - PDFs de prueba no se commitean

### Pendiente ⏳

1. **Rate limiting**
   - Middleware para limitar requests por IP
   - Prevenir abuse de endpoint de upload

2. **API authentication**
   - API keys para endpoints públicos
   - OAuth 2.0 para integraciones futuras

3. **Validación de archivos**
   - Tamaño máximo de archivo (actualmente ilimitado)
   - Validación de contenido (magic bytes, no solo extensión)
   - Sanitización de nombres de archivo

4. **CORS específico**
   - Actualmente permite todos los orígenes
   - Configurar whitelist de dominios

5. **Logging y monitoring**
   - Cloud Logging para auditoría
   - Alertas de errores en Cloud Run

## 📂 Estructura de Archivos del Proyecto

```
D:/Proyectos/prueba_tecnica_DiagnoVet/
│
├── app/                                # Código fuente principal
│   ├── __init__.py                    # Marca app/ como paquete Python
│   │
│   ├── main.py                        # [69 líneas] FastAPI app principal
│   │   ├── app = FastAPI()
│   │   ├── Inicialización de servicios:
│   │   │   ├── pdf_processor = PDFProcessor()
│   │   │   ├── storage_service = GCPStorageService(bucket_name, project_id)
│   │   │   └── firestore_service = FirestoreService(project_id)
│   │   ├── POST /upload-report
│   │   ├── GET /reports/{report_id}
│   │   └── GET /reports
│   │
│   ├── models.py                      # [45 líneas] Modelos Pydantic
│   │   ├── class VeterinaryReport(BaseModel):
│   │   │   ├── id: str
│   │   │   ├── pdf_filename: str
│   │   │   ├── patient_name: Optional[str]
│   │   │   ├── owner_name: Optional[str]
│   │   │   ├── veterinarian_name: Optional[str]
│   │   │   ├── diagnosis: Optional[str]
│   │   │   ├── recommendations: Optional[str]
│   │   │   ├── image_urls: List[str]
│   │   │   ├── upload_date: str
│   │   │   └── status: str
│   │   ├── class UploadResponse(BaseModel):
│   │   │   ├── report_id: str
│   │   │   └── message: str
│   │   └── class ErrorResponse(BaseModel):
│   │       ├── error: str
│   │       └── detail: str
│   │
│   ├── config.py                      # [23 líneas] Configuración con env vars
│   │   ├── class Settings(BaseSettings):
│   │   │   ├── gcp_project_id: str
│   │   │   ├── gcs_bucket_name: str
│   │   │   ├── gcp_location: str = "us-central1"
│   │   │   └── environment: str = "development"
│   │   └── @lru_cache def get_settings() -> Settings
│   │
│   └── services/                      # Lógica de negocio por responsabilidad
│       ├── __init__.py
│       │
│       ├── pdf_processor.py           # [78 líneas] Procesamiento de PDFs
│       │   └── class PDFProcessor:
│       │       ├── extract_text(pdf_path: str) -> str
│       │       │   └── Usa PyPDF2.PdfReader para leer texto
│       │       ├── extract_images(pdf_path: str, report_id: str) -> List[str]
│       │       │   ├── Itera páginas del PDF
│       │       │   ├── Extrae XObject images
│       │       │   ├── Soporta: DCTDecode (JPEG), FlateDecode/JPXDecode (PNG)
│       │       │   ├── Guarda en extracted_images/{report_id}/
│       │       │   └── Retorna lista de paths locales
│       │       └── extract_fields_with_document_ai(pdf_path: str) -> Dict
│       │           └── [PENDIENTE] Retorna {} actualmente
│       │
│       ├── gcp_storage.py             # [54 líneas] Cliente Cloud Storage
│       │   └── class GCPStorageService:
│       │       ├── __init__(bucket_name: str, project_id: str)
│       │       │   ├── self.client = storage.Client(project=project_id)
│       │       │   └── self.bucket = client.get_bucket(bucket_name)
│       │       ├── upload_image(local_path: str, dest_blob_name: str) -> str
│       │       │   ├── Sube archivo a bucket
│       │       │   ├── Retorna blob.public_url
│       │       │   └── NO llama make_public() (uniform access enabled)
│       │       ├── upload_multiple_images(paths: List[str], report_id: str) -> List[str]
│       │       │   ├── Por cada imagen:
│       │       │   │   └── upload_image(path, f"reports/{report_id}/{filename}")
│       │       │   └── Retorna lista de URLs públicas
│       │       └── delete_image(blob_name: str) -> bool
│       │
│       └── firestore_db.py            # [62 líneas] Cliente Firestore
│           └── class FirestoreService:
│               ├── __init__(project_id: str)
│               │   ├── self.db = firestore.Client(project=project_id)
│               │   └── self.collection = db.collection("reports")
│               ├── save_report(report_data: dict) -> str
│               │   ├── doc_ref = collection.document(report_data["id"])
│               │   ├── doc_ref.set(report_data)
│               │   └── Retorna report_id
│               ├── get_report(report_id: str) -> Optional[dict]
│               │   ├── doc = collection.document(report_id).get()
│               │   ├── if doc.exists: return doc.to_dict()
│               │   └── else: return None
│               ├── list_reports(limit: int = 100) -> List[dict]
│               │   └── Retorna [doc.to_dict() for doc in collection.limit(limit).stream()]
│               ├── update_report(report_id: str, updates: dict) -> bool
│               └── delete_report(report_id: str) -> bool
│
├── uploads/                           # PDFs subidos temporalmente (gitignored)
│   └── [report_id]_[filename].pdf
│
├── extracted_images/                  # Imágenes extraídas localmente (gitignored)
│   └── [report_id]/
│       ├── [report_id]_image_0.jpg
│       ├── [report_id]_image_1.png
│       └── ...
│
├── venv/                              # Entorno virtual Python (gitignored)
│   └── [dependencias instaladas]
│
├── requirements.txt                   # [12 dependencias] Versiones fijas
│   ├── fastapi==0.115.0
│   ├── uvicorn==0.32.0
│   ├── PyPDF2==3.0.1
│   ├── Pillow==10.4.0
│   ├── google-cloud-storage==2.18.2
│   ├── google-cloud-firestore==2.19.0
│   ├── google-cloud-documentai==2.30.0
│   ├── pydantic==2.8.2              # Fixed: evita compilación Rust
│   ├── pydantic-settings==2.3.4
│   ├── python-multipart==0.0.12
│   └── [otras dependencias transitivas]
│
├── .env                               # Variables de entorno (gitignored, sensible)
│   ├── GCP_PROJECT_ID=project-630f5850-5bf8-4280-808
│   ├── GCS_BUCKET_NAME=diagnovet-reports-images
│   └── ENVIRONMENT=development
│
├── .env.example                       # Template de .env (commiteado)
│   ├── GCP_PROJECT_ID=your-project-id
│   ├── GCS_BUCKET_NAME=your-bucket-name
│   └── ENVIRONMENT=development
│
├── .gitignore                         # Exclusiones de Git
│   ├── venv/
│   ├── __pycache__/
│   ├── .env
│   ├── uploads/
│   ├── extracted_images/
│   ├── credentials/
│   └── *.pyc
│
├── Dockerfile                         # [PENDIENTE] Configuración para Cloud Run
│
├── README.md                          # [~450 líneas] Documentación completa
│   ├── Descripción del proyecto
│   ├── Arquitectura con diagrama ASCII
│   ├── Stack tecnológico detallado (cada lib con justificación)
│   ├── Instalación paso a paso (7 pasos)
│   ├── Documentación de endpoints (3 endpoints)
│   ├── Testing manual con ejemplos
│   ├── Estructura del proyecto
│   ├── Decisiones arquitectónicas (5 secciones)
│   ├── Estado del proyecto (Fases 1-6)
│   ├── Seguridad implementada
│   └── Recursos y referencias
│
└── PROJECT_CONTEXT.md                 # [ESTE ARCHIVO] Prompt completo del proyecto
    ├── Objetivo del proyecto
    ├── Contexto del desarrollador
    ├── Estado actual (fases)
    ├── Arquitectura técnica detallada
    ├── Configuración de seguridad
    ├── Estructura de archivos
    ├── Problemas resueltos
    ├── Testing realizado
    └── Próximos pasos
```

## 🐛 Problemas Resueltos Durante Desarrollo

### 1. Error de compilación de Pydantic con Rust

**Error:**

```
Failed to build pydantic-core==2.23.4
error: can't find Rust compiler
```

**Causa:** Pydantic 2.9.2 requería pydantic-core 2.23.4 que necesita compilación de Rust. Conflicto con instalación existente de rustup.

**Solución:**

```bash
# Downgrade a versión precompilada
pip install pydantic==2.8.2 pydantic-settings==2.3.4
```

**Lección aprendida:** Fijar versiones en requirements.txt para evitar breaking changes.

### 2. Política de organización bloqueando creación de Service Account Keys

**Error:**

```
ERROR: (gcloud.iam.service-accounts.keys.create) PERMISSION_DENIED:
Service account key creation is disabled by the organization policy
```

**Causa:** Política `iam.disableServiceAccountKeyCreation` activa en la organización GCP (seguridad enterprise).

**Solución:**
Usar Application Default Credentials en lugar de JSON keys:

```bash
gcloud auth application-default login
```

**Lección aprendida:** ADC es más seguro y recomendado por Google. JSON keys solo para casos específicos.

### 3. Error de ACL en Cloud Storage con uniform bucket-level access

**Error:**

```
400 Cannot get legacy ACL for an object when uniform bucket-level access is enabled
```

**Causa:** Intentar llamar `blob.make_public()` en bucket con uniform access enabled.

**Solución:**
Configurar permisos a nivel de bucket y no llamar make_public():

```bash
gsutil iam ch allUsers:objectViewer gs://diagnovet-reports-images
```

**Código eliminado:**

```python
# NO hacer esto con uniform access:
# blob.make_public()

# Solo hacer upload y retornar public_url:
blob.upload_from_filename(local_path)
return blob.public_url
```

**Lección aprendida:** Uniform bucket-level access simplifica permisos pero cambia API.

### 4. Firestore API no habilitada (403 SERVICE_DISABLED)

**Error:**

```
403 Cloud Firestore API has not been used in project before or it is disabled
```

**Causa:** API de Firestore no habilitada en el proyecto GCP.

**Solución:**

```bash
gcloud services enable firestore.googleapis.com
```

**Lección aprendida:** Siempre habilitar APIs antes de usar servicios GCP.

### 5. Base de datos Firestore no existe (404)

**Error:**

```
404 Database '(default)' does not exist in project 'project-630f5850-5bf8-4280-808'
```

**Causa:** API habilitada pero base de datos no creada.

**Solución:**

```bash
gcloud firestore databases create --location=us-central1
# O via consola: https://console.cloud.google.com/firestore/databases
```

**Lección aprendida:** Habilitar API ≠ crear recursos. Dos pasos separados.

### 6. Errores de sintaxis en firestore_db.py durante edición

**Error:**

```
SyntaxError: unterminated string literal
SyntaxError: unexpected EOF while parsing
```

**Causa:** Edición manual con errores de copy-paste, strings sin cerrar, paréntesis desbalanceados.

**Solución:**
Eliminar archivo y recrear desde cero con código limpio.

**Lección aprendida:** Para archivos problemáticos, mejor recrear que intentar arreglar errores compuestos.

## 🧪 Testing Realizado

### Testing Manual con Postman

**PDF de prueba:** "Estudio Radiográfico Ramón.pdf"

**Test 1: POST /upload-report**

- Request:
  ```
  POST http://localhost:8000/upload-report
  Body: form-data
    file: [Estudio Radiográfico Ramón.pdf]
  ```
- Response:
  ```json
  {
    "report_id": "62b7d119",
    "message": "Reporte procesado. 13 imágenes extraídas y 13 subidas a Cloud Storage."
  }
  ```
- ✅ PASS: 13 imágenes detectadas y procesadas

**Test 2: Verificar Cloud Storage**

- Console: https://console.cloud.google.com/storage/browser/diagnovet-reports-images/reports/62b7d119
- Resultado: 13 archivos .jpg/.png en carpeta
- URLs públicas accesibles: ✅ PASS

**Test 3: Verificar Firestore**

- Console: https://console.cloud.google.com/firestore/databases/-default-/data/panel/reports/62b7d119
- Resultado: Documento con metadata completa
- image_urls array con 13 URLs: ✅ PASS

**Test 4: GET /reports/62b7d119**

- Request:
  ```
  GET http://localhost:8000/reports/62b7d119
  ```
- Response:
  ```json
  {
    "id": "62b7d119",
    "pdf_filename": "Estudio Radiográfico Ramón.pdf",
    "patient_name": null,
    "owner_name": null,
    "veterinarian_name": null,
    "diagnosis": null,
    "recommendations": null,
    "image_urls": [
      "https://storage.googleapis.com/diagnovet-reports-images/reports/62b7d119/62b7d119_image_2.png",
      "https://storage.googleapis.com/diagnovet-reports-images/reports/62b7d119/62b7d119_image_3.jpg",
      ...
    ],
    "upload_date": "2026-02-04T20:15:30.123456",
    "status": "processed"
  }
  ```
- ✅ PASS: Datos correctos, URLs funcionan

**Test 5: GET /reports**

- Request:
  ```
  GET http://localhost:8000/reports
  ```
- Response:
  ```json
  {
    "total_reports": 1,
    "reports": [
      {
        "id": "62b7d119",
        "pdf_filename": "Estudio Radiográfico Ramón.pdf",
        "image_urls": [...],
        "upload_date": "2026-02-04T20:15:30.123456",
        "status": "processed"
      }
    ]
  }
  ```
- ✅ PASS: Lista correcta de reportes

### Testing de Documentación Automática

**Swagger UI:**

- URL: http://localhost:8000/docs
- ✅ Muestra 3 endpoints
- ✅ Permite testing interactivo
- ✅ Schemas visibles (VeterinaryReport, UploadResponse)

**ReDoc:**

- URL: http://localhost:8000/redoc
- ✅ Documentación alternativa generada correctamente

### Testing de Comandos GCP

**gcloud CLI:**

```bash
# Verificar autenticación
gcloud auth list
# ✅ PASS: Cuenta activa mostrada

# Verificar proyecto
gcloud config get-value project
# ✅ PASS: project-630f5850-5bf8-4280-808

# Verificar APIs habilitadas
gcloud services list --enabled | grep -E 'storage|firestore'
# ✅ PASS: storage.googleapis.com, firestore.googleapis.com
```

**gsutil:**

```bash
# Listar bucket
gsutil ls gs://diagnovet-reports-images/reports/
# ✅ PASS: Carpeta 62b7d119/ visible

# Verificar permisos
gsutil iam get gs://diagnovet-reports-images
# ✅ PASS: allUsers tiene roles/storage.objectViewer
```

## 📝 Comandos Útiles de Referencia

### Desarrollo Local

```bash
# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Ejecutar servidor desarrollo
python -m uvicorn app.main:app --reload

# Ejecutar en puerto específico
python -m uvicorn app.main:app --reload --port 8080

# Ver logs detallados
python -m uvicorn app.main:app --reload --log-level debug
```

### GCP - Configuración General

```bash
# Login con cuenta Google
gcloud auth login

# Configurar Application Default Credentials
gcloud auth application-default login

# Ver proyecto actual
gcloud config get-value project

# Cambiar proyecto
gcloud config set project PROJECT_ID

# Ver credenciales activas
gcloud auth list

# Listar APIs habilitadas
gcloud services list --enabled

# Habilitar API
gcloud services enable <API_NAME>
```

### GCP - Cloud Storage

```bash
# Crear bucket
gsutil mb -p PROJECT_ID -l us-central1 gs://BUCKET_NAME

# Listar buckets
gsutil ls

# Listar contenido de bucket
gsutil ls gs://BUCKET_NAME

# Subir archivo
gsutil cp local_file.pdf gs://BUCKET_NAME/path/

# Hacer bucket público (lectura)
gsutil iam ch allUsers:objectViewer gs://BUCKET_NAME

# Ver permisos del bucket
gsutil iam get gs://BUCKET_NAME

# Eliminar bucket (¡cuidado!)
gsutil rm -r gs://BUCKET_NAME
```

### GCP - Firestore

```bash
# Habilitar API
gcloud services enable firestore.googleapis.com

# Crear base de datos
gcloud firestore databases create --location=us-central1

# Listar bases de datos
gcloud firestore databases list

# Ver datos (via consola web)
# https://console.cloud.google.com/firestore/databases/-default-/data/panel
```

### GCP - Document AI (Pendiente)

```bash
# Habilitar API
gcloud services enable documentai.googleapis.com

# Listar procesadores
gcloud ai document-processors list --location=us

# Ver logs de Document AI
gcloud logging read "resource.type=documentai_processor" --limit=20
```

### GCP - Cloud Run (Pendiente)

```bash
# Build imagen con Cloud Build
gcloud builds submit --tag gcr.io/PROJECT_ID/diagnovet-api

# Deploy a Cloud Run
gcloud run deploy diagnovet-api \
  --image gcr.io/PROJECT_ID/diagnovet-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars KEY=VALUE

# Listar servicios
gcloud run services list

# Ver detalles de servicio
gcloud run services describe diagnovet-api --region us-central1

# Ver logs en tiempo real
gcloud run logs tail diagnovet-api --region us-central1

# Eliminar servicio
gcloud run services delete diagnovet-api --region us-central1
```

### Git

```bash
# Ver estado
git status

# Agregar cambios
git add .

# Commit con mensaje
git commit -m "feat: descripción del cambio"

# Ver log de commits
git log --oneline

# Ver diferencias
git diff
```

## 🎓 Aprendizajes Clave del Proyecto

### Tecnologías GCP Aprendidas

1. **Cloud Storage**
   - Concepto de buckets y objetos
   - IAM y permisos (uniform vs legacy ACL)
   - URLs públicas vs signed URLs
   - Organización de datos por prefijos (carpetas virtuales)

2. **Firestore**
   - Diferencia entre Native mode y Datastore mode
   - Modelo de colecciones y documentos
   - Queries simples vs complejas
   - Cuándo usar NoSQL vs SQL

3. **Application Default Credentials**
   - Cómo funciona la autenticación en GCP
   - Diferencia entre user credentials y service accounts
   - Por qué es más seguro que JSON keys

4. **Document AI** (próximo)
   - Diferencia entre OCR tradicional y ML-based OCR
   - Form parsing vs custom extraction

### Decisiones Arquitectónicas Aprendidas

1. **Separación de responsabilidades**
   - Servicios independientes (pdf_processor, gcp_storage, firestore_db)
   - Cada clase con responsabilidad única
   - Fácil de testear y modificar

2. **Progresión incremental**
   - Fase 1: Local processing (sin costos)
   - Fase 2: Cloud storage (persistencia básica)
   - Fase 3: ML services (funcionalidad avanzada)
   - Mejor que hacer todo de una vez

3. **Configuration management**
   - Variables de entorno para configuración
   - .env para desarrollo, env vars en Cloud Run para producción
   - Nunca hardcodear credenciales

4. **Modelo de datos flexible**
   - Campos Optional[str] para datos que vendrán después
   - Array de URLs en vez de embeber imágenes
   - Status field para tracking de procesamiento

### Habilidades de Debugging

1. **Leer errores de GCP efectivamente**
   - Identificar códigos de error (403, 404, 400)
   - Interpretar mensajes de APIs no habilitadas
   - Buscar en documentación oficial

2. **Validar configuración paso a paso**
   - No asumir que todo funciona
   - Verificar cada servicio independientemente
   - Usar consolas web para inspeccionar estado

3. **Rollback cuando es necesario**
   - Downgrade de dependencias problemáticas
   - Recrear archivos en vez de arreglar código roto
   - Volver a arquitectura más simple si es necesario

## 🚀 Próximos Pasos Inmediatos

### Para completar el challenge (prioridad)

1. **Implementar Document AI** (30-45 min)
   - Habilitar API
   - Crear procesador
   - Codificar extract_fields_with_document_ai()
   - Testing con PDF real

2. **Deploy a Cloud Run** (20-30 min)
   - Build imagen Docker
   - Deploy con gcloud run deploy
   - Testing en producción

3. **Grabar video demo** (45-60 min)
   - Script del video
   - Grabación con Loom/OBS
   - Upload a YouTube unlisted

4. **Entregar challenge** (15 min)
   - Repo GitHub privado
   - Email a recruiter con links
   - Confirmar recepción

### Para mejorar el proyecto (opcional, tiempo permitiendo)

1. **Tests automatizados**
   - pytest para servicios
   - Tests de integración para endpoints

2. **CI/CD pipeline**
   - GitHub Actions para tests
   - Deploy automático en merge a main

3. **Mejoras de UI**
   - Frontend simple con React/Vue
   - Drag & drop de PDFs
   - Visualización de reportes

4. **Features adicionales**
   - Búsqueda de reportes por paciente/fecha
   - Filtros y paginación
   - Exportar a PDF con formato

## 📧 Para Usar Este Contexto

**Si eres otra IA ayudando con este proyecto:**

Este documento contiene TODO el contexto necesario. Puedes:

- Continuar desde donde se quedó (Fase 2 completada)
- Implementar Fase 3 (Document AI) con toda la info necesaria
- Explicar cualquier decisión técnica tomada
- Ayudar a preparar el video demo
- Debuggear problemas con conocimiento completo del stack

**Si eres un revisor técnico (recruiter de diagnoVET):**

Este documento muestra:

- Proceso de pensamiento y toma de decisiones
- Capacidad de aprendizaje incremental de tecnologías nuevas
- Documentación exhaustiva (importante para trabajo en equipo)
- Honestidad sobre nivel de experiencia actual
- Enfoque en entender el "por qué" de cada decisión

**Si eres Yeison (el desarrollador) en el futuro:**

Este documento te sirve como:

- Referencia completa del proyecto
- Justificaciones de decisiones para el video
- Material de estudio de GCP
- Template para futuros proyectos similares

---

**Última actualización:** 4 de febrero de 2026  
**Versión:** 1.0.0  
**Autor original:** Yeison (con asistencia de AI)  
**Proyecto:** DiagnoVET Backend Challenge  
**Estado:** Fases 1-2 completadas, listo para Fase 3 (Document AI)
