# 🏥 DiagnoVET - Backend Challenge

API REST para procesamiento automatizado de reportes veterinarios en PDF usando Google Cloud Platform.

## 📋 Descripción

Este proyecto procesa reportes médicos veterinarios en PDF, extrayendo imágenes y metadata de forma estructurada.

**Funcionalidades implementadas:**

- ✅ Extracción de imágenes del PDF con PyPDF2
- ✅ Almacenamiento en Cloud Storage con URLs públicas
- ✅ Persistencia en Firestore con metadata de reportes
- ✅ API REST con 3 endpoints (upload, get, list)
- ✅ Extracción de datos con Document AI OCR Processor
- ✅ Detección automática de: paciente, propietario, veterinario, diagnóstico
- ✅ Soporte para múltiples formatos de reportes médicos

**Próximamente:**

- ⏳ Deploy a Cloud Run (serverless)
- ⏳ Tests automatizados

## 🏗️ Arquitectura

```
PDF → FastAPI → PyPDF2 (extrae imágenes) → Cloud Storage (almacena)
              → Document AI (OCR + extracción de campos)
              → Firestore (metadata + campos extraídos)
              → JSON con URLs públicas + datos estructurados
```

**Stack tecnológico:**

- **FastAPI** - Framework web Python moderno
- **PyPDF2** - Extracción de imágenes de PDFs
- **Google Cloud Storage** - Almacenamiento de imágenes
- **Firestore** - Base de datos NoSQL
- **Document AI** ✅ - OCR inteligente con extracción de campos
- **Cloud Run** ⏳ - Deploy serverless (próximamente)

## 📊 Estado del Proyecto

### ✅ Fase 1: Procesamiento Local + Cloud Storage (Completada)

- [x] API FastAPI funcionando
- [x] Endpoint POST /upload-report
- [x] Extracción de texto de PDFs
- [x] Extracción de imágenes de PDFs
- [x] Subida de imágenes a Cloud Storage
- [x] URLs públicas de imágenes
- [x] Autenticación con Application Default Credentials

### ✅ Fase 2: Firestore Database (Completada)

- [x] Integración con Firestore
- [x] Guardar metadata de reportes en base de datos
- [x] Endpoint GET /reports/{id} con datos reales desde Firestore
- [x] Endpoint GET /reports (listar todos los reportes)
- [x] Colección "reports" con estructura JSON
- [x] URLs de imágenes almacenadas en metadata

### ✅ Fase 3: Document AI (Completada)

- [x] Habilitar Document AI API
- [x] Crear procesador OCR en región US
- [x] Implementar extracción de campos con regex optimizado
- [x] Extraer: paciente, propietario, veterinario, diagnóstico, recomendaciones
- [x] Testing con múltiples formatos de reportes (Chester, Ramón)
- [x] Integración completa en endpoint POST /upload-report

### ⏳ Fase 4: Deploy y Finalización (Pendiente)

- [ ] Deploy a Cloud Run
- [ ] Testing en producción
- [ ] Video demo explicativo (5 min)
- [ ] Documentación técnica completa

## 🚀 Instalación y Configuración

### Prerrequisitos

- Python 3.11+
- Cuenta de Google Cloud Platform
- Google Cloud CLI (`gcloud`)
- Docker (para deploy final)

### Paso 1: Clonar y configurar entorno

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno (Windows)
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### Paso 2: Configurar Google Cloud

```bash
# Instalar Google Cloud CLI
# Descargar de: https://cloud.google.com/sdk/docs/install

# Autenticar
gcloud auth application-default login

# Configurar proyecto
gcloud config set project TU_PROJECT_ID
```

### Paso 3: Crear Cloud Storage Bucket

```bash
# Habilitar Cloud Storage API
gcloud services enable storage.googleapis.com

# Crear bucket (debe ser único globalmente)
gsutil mb -p TU_PROJECT_ID -l us-central1 gs://diagnovet-reports-images

# Hacer el bucket público (para acceso a imágenes)
gsutil iam ch allUsers:objectViewer gs://diagnovet-reports-images
```

### Paso 4: Configurar Firestore

```bash
# Habilitar Firestore API
gcloud services enable firestore.googleapis.com
```

### Paso 5: Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
GCP_PROJECT_ID=tu-proyecto-id
GCS_BUCKET_NAME=diagnovet-reports-images
ENVIRONMENT=development
```

### Paso 6: Ejecutar localmente

```bash
# Modo desarrollo con recarga automática
python -m uvicorn app.main:app --reload

# La API estará disponible en: http://localhost:8000
# Documentación interactiva: http://localhost:8000/docs
```

## 📡 Endpoints Disponibles

### ✅ `POST /upload-report`

Sube un PDF y extrae imágenes automáticamente.

**Estado:** Funcionando completamente

**Request (usando cURL):**

```bash
curl -X POST "http://localhost:8000/upload-report" \
  -F "file=@/ruta/a/tu/reporte.pdf"
```

**Request (usando Postman):**

- Method: POST
- URL: `http://localhost:8000/upload-report`
- Body → form-data
- Key: `file` (tipo: File)
- Value: Seleccionar archivo PDF

**Response:**

```json
{
  "report_id": "62b7d119",
  "message": "Reporte procesado. 13 imágenes extraídas y 13 subidas a Cloud Storage."
}
```

**Flujo de procesamiento:**

1. ✅ Recibe el PDF
2. ✅ Extrae texto del documento
3. ✅ Extrae imágenes embebidas
4. ✅ Sube imágenes a Cloud Storage
5. ✅ Genera URLs públicas
6. ✅ Guarda metadata en Firestore

### ✅ `GET /reports/{report_id}`

Obtiene la información estructurada de un reporte.

**Estado:** Funcionando completamente

**Response:**

```json
{
  "id": "419616cd",
  "pdf_filename": "Estudio Radiográfico Ramón.pdf",
  "patient_name": "Ramón",
  "owner_name": "Simonetti",
  "veterinarian_name": "Ghersevich Carolina",
  "diagnosis": "• Depósito de material de radiodensidad mineral en laterales de espacio intervertebral entre vértebras T13-L1. • Patrón pulmonar bronquial panlobar moderado...",
  "recommendations": null,
  "image_urls": [
    "https://storage.googleapis.com/diagnovet-reports-images/reports/419616cd/419616cd_image_2.png",
    "https://storage.googleapis.com/diagnovet-reports-images/reports/419616cd/419616cd_image_3.jpg"
  ],
  "upload_date": "2026-02-06T00:45:12.123456",
  "status": "processed"
}
```

**Nota:** Los campos se extraen automáticamente con Document AI. Si algún campo es `null`, significa que no se detectó en el PDF.

### ✅ `GET /reports`

Lista todos los reportes disponibles.

**Estado:** Funcionando completamente

**Response:**

```json
{
  "total_reports": 3,
  "reports": [
    {
      "id": "62b7d119",
      "pdf_filename": "Estudio Radiográfico Ramón.pdf",
      "image_urls": [...]
    },
    ...
  ]
}
```

## 🧪 Testing Manual

### Probar subida de PDF

**En Postman:**

1. POST `http://localhost:8000/upload-report`
2. Body → form-data
3. Key: `file` (tipo: File)
4. Value: Seleccionar PDF
5. Send

**Verificar resultados:**

- Carpetas locales: `uploads/` y `extracted_images/`
- Cloud Storage: https://console.cloud.google.com/storage/browser/diagnovet-reports-images/reports
- Deberías ver una carpeta con el `report_id` y las imágenes dentro

### Ver documentación interactiva

Abre en tu navegador: http://localhost:8000/docs

Ahí puedes probar todos los endpoints directamente.

## 🐳 Deploy a Cloud Run (Pendiente)

```bash
# Build de imagen
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/diagnovet-api

# Deploy
gcloud run deploy diagnovet-api \
  --image gcr.io/YOUR_PROJECT_ID/diagnovet-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## 📁 Estructura del Proyecto

```
diagnovet-challenge/
├── app/
│   ├── main.py              # API FastAPI
│   ├── models.py            # Modelos de datos
│   ├── config.py            # Configuración
│   └── services/
│       ├── pdf_processor.py # Procesamiento de PDFs
│       ├── gcp_storage.py   # Cloud Storage
│       └── firestore_db.py  # Firestore DB
├── uploads/                 # PDFs temporales
├── extracted_images/        # Imágenes extraídas
├── requirements.txt         # Dependencias
├── Dockerfile              # Configuración Docker
└── README.md
```

## 🎯 Decisiones Técnicas

### ¿Por qué FastAPI?

- ✅ Validación automática de datos con Pydantic
- ✅ Documentación interactiva automática (Swagger)
- ✅ Alto rendimiento (async/await)
- ✅ Type hints nativos para mejor desarrollo

### ¿Por qué Firestore?

- ✅ NoSQL flexible (ideal para datos semi-estructurados)
- ✅ Consultas en tiempo real
- ✅ Escalabilidad automática sin configuración
- ✅ Setup rápido (sin esquemas SQL)
- ✅ Integración nativa con otros servicios GCP
- ✅ SDK simple y directo

### Arquitectura de datos en Firestore

**Colección:** `reports`  
**Estructura de documento:**

```json
{
  "id": "62b7d119",
  "pdf_filename": "reporte.pdf",
  "patient_name": null,
  "owner_name": null,
  "veterinarian_name": null,
  "diagnosis": null,
  "recommendations": null,
  "image_urls": ["https://storage.googleapis.com/..."],
  "upload_date": "2026-02-04T20:15:30.123456",
  "status": "processed"
}
```

**Nota:** Los campos `patient_name`, `diagnosis`, etc. se llenarán con Document AI en la Fase 3.

### ¿Por qué PyPDF2 para extracción local?

- ✅ Librería estable y probada
- ✅ Funciona sin dependencias externas pesadas
- ✅ Suficiente para extraer imágenes embebidas
- ✅ Permite desarrollo/testing sin costos de API

### ¿Por qué Application Default Credentials?

- ✅ Más seguro que archivos JSON de service accounts
- ✅ No hay riesgo de exponer credenciales en Git
- ✅ Funciona igual en local y en Cloud Run
- ✅ Recomendado por Google Cloud

## 📝 Próximos Pasos

### Fase 3: Document AI

- [ ] Habilitar Document AI API
- [ ] Configurar procesador de formularios
- [ ] Implementar extracción de campos específicos
- [ ] Actualizar reportes con datos extraídos
- [ ] Validar precisión de extracción

### Fase 4: Deploy y Optimización

- [ ] Crear Dockerfile optimizado
- [ ] Deploy a Cloud Run
- [ ] Configurar CI/CD con GitHub Actions
- [ ] Tests automatizados
- [ ] Monitoreo con Cloud Logging

## 🔒 Seguridad Implementada

- ✅ Application Default Credentials (sin archivos JSON expuestos)
- ✅ Validación de tipos de archivo (solo PDFs)
- ✅ Variables sensibles en .env (no en código)
- ✅ .gitignore configurado (credenciales excluidas)
- ⏳ Rate limiting (próximamente)
- ⏳ Autenticación con API Keys (próximamente)

## 👤 Autor

**Yeison** - Backend Engineer Challenge para DiagnoVET

## 📄 Licencia

Este proyecto es parte de un challenge técnico.
