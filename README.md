# 🏥 DiagnoVET - Backend Challenge

API REST para procesamiento automatizado de reportes de ultrasonido veterinario usando Google Cloud Platform.

## 📋 Descripción

Este proyecto extrae información estructurada de reportes médicos en PDF, incluyendo:
- ✅ **Extracción de imágenes** del PDF
- ✅ **Almacenamiento en Cloud Storage** con URLs públicas
- ⏳ **Datos del paciente** (con Document AI - próximamente)
- ⏳ **Información del veterinario** (con Document AI - próximamente)
- ⏳ **Diagnóstico y recomendaciones** (con Document AI - próximamente)

## 🏗️ Arquitectura

```
Usuario → FastAPI → Cloud Storage + Firestore
                ↓
         (Próximamente: Document AI)
```

**Stack tecnológico:**
- ✅ **FastAPI**: Framework web Python moderno
- ✅ **Google Cloud Storage**: Almacenamiento de imágenes
- ✅ **PyPDF2**: Extracción de imágenes de PDFs
- ⏳ **Firestore**: Base de datos NoSQL (próximamente)
- ⏳ **Google Document AI**: OCR y extracción inteligente (próximamente)
- ⏳ **Google Cloud Run**: Hosting serverless (deploy final)

## 📊 Estado del Proyecto

### ✅ Fase 1 Completada: Procesamiento Local + Cloud Storage
- [x] API FastAPI funcionando
- [x] Endpoint POST /upload-report
- [x] Extracción de texto de PDFs
- [x] Extracción de imágenes de PDFs
- [x] Subida de imágenes a Cloud Storage
- [x] URLs públicas de imágenes
- [x] Autenticación con Application Default Credentials

### ⏳ Fase 2: En Desarrollo
- [ ] Integración con Firestore (base de datos)
- [ ] Integración con Document AI (OCR inteligente)
- [ ] Endpoint GET /reports/{id} con datos reales
- [ ] Endpoint GET /reports (listar todos)

### ⏳ Fase 3: Pendiente
- [ ] Deploy a Cloud Run
- [ ] CI/CD con GitHub Actions
- [ ] Video demo explicativo

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

### Paso 3: Crear Bucket de Cloud Storage

```bash
# Crear bucket (debe ser único globalmente)
gsutil mb -p TU_PROJECT_ID gs://diagnovet-reports-images

# Hacer el bucket público (para acceso a imágenes)
gsutil iam ch allUsers:objectViewer gs://diagnovet-reports-images
```

### Paso 4: Configurar variables de entorno

```bash
# Editar archivo .env con tus valores
GCP_PROJECT_ID=tu-proyecto-id
GCS_BUCKET_NAME=diagnovet-reports-images
ENVIRONMENT=development
```

### Paso 5: Ejecutar localmente

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
- Body: form-data
  - Key: `file` (tipo: File)
  - Value: Seleccionar archivo PDF

**Response:**
```json
{
  "report_id": "ba5b080e",
  "message": "Reporte procesado. 13 imágenes extraídas y 13 subidas a Cloud Storage."
}
```

**Lo que hace:**
1. ✅ Recibe el PDF
2. ✅ Extrae texto del documento
3. ✅ Extrae imágenes embebidas
4. ✅ Sube imágenes a Cloud Storage
5. ✅ Genera URLs públicas
6. ⏳ Guarda metadata en Firestore (próximamente)

### ⏳ `GET /reports/{report_id}`
Obtiene la información estructurada de un reporte.

**Estado:** En desarrollo (retorna datos de ejemplo)

**Response (actual):**
```json
{
  "id": "ba5b080e",
  "patient_name": "Max (ejemplo local)",
  "owner_name": "Juan Pérez (ejemplo)",
  "veterinarian_name": "Dr. García (ejemplo)",
  "diagnosis": "Pendiente de procesamiento con Document AI",
  "recommendations": "En desarrollo",
  "image_urls": [],
  "pdf_filename": "ejemplo.pdf",
  "upload_date": "2026-02-04T19:12:00"
}
```

### ⏳ `GET /reports`
Lista todos los reportes disponibles.

**Estado:** En desarrollo

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
- ✅ Fácil de testear
- ✅ Type hints nativos de Python

### ¿Por qué Cloud Storage?
- ✅ Escalabilidad ilimitada para archivos
- ✅ URLs públicas automáticas
- ✅ Durabilidad 99.999999999%
- ✅ Integración nativa con otros servicios GCP
- ✅ Pago por uso (muy económico)

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

### Próximas decisiones (Firestore vs Cloud SQL)
**Elegiremos Firestore porque:**
- NoSQL flexible (ideal para datos semi-estructurados)
- Consultas en tiempo real
- Escalabilidad automática
- Setup más rápido (sin esquemas)

### Próximas decisiones (Document AI)
**Para extracción inteligente de campos:**
- OCR avanzado con ML
- Extracción de entidades específicas
- Soporta documentos médicos complejos
- Mejor precisión que OCR tradicional

## 📝 Próximos Pasos

### Fase 2: Firestore + Document AI (En progreso)
- [ ] Activar Firestore en GCP
- [ ] Implementar FirestoreService completo
- [ ] Configurar Document AI processor
- [ ] Extraer campos específicos (paciente, diagnóstico, etc.)
- [ ] Guardar metadata en Firestore
- [ ] Actualizar GET /reports/{id} con datos reales

### Fase 3: Deploy y Optimización
- [ ] Crear Dockerfile optimizado
- [ ] Deploy a Cloud Run
- [ ] Configurar CI/CD con GitHub Actions
- [ ] Tests automatizados
- [ ] Monitoreo con Cloud Logging

### Fase 4: Documentación Final
- [ ] Video demo (5 min)
- [ ] Explicación de arquitectura
- [ ] Decisiones técnicas justificadas
- [ ] README completo

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
