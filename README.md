# 🏥 DiagnoVET - Backend Challenge

API REST para procesamiento automatizado de reportes de ultrasonido veterinario usando Google Cloud Platform.

## 📋 Descripción

Este proyecto extrae información estructurada de reportes médicos en PDF, incluyendo:
- **Datos del paciente** (animal)
- **Datos del dueño**
- **Información del veterinario**
- **Diagnóstico médico**
- **Recomendaciones**
- **Imágenes** extraídas del PDF

## 🏗️ Arquitectura

```
Usuario → FastAPI → Document AI → Firestore + Cloud Storage
```

**Stack tecnológico:**
- **FastAPI**: Framework web Python moderno
- **Google Cloud Run**: Hosting serverless
- **Google Document AI**: OCR y extracción inteligente
- **Google Cloud Storage**: Almacenamiento de imágenes
- **Firestore**: Base de datos NoSQL

## 🚀 Instalación Local

### Prerrequisitos
- Python 3.11+
- Docker (para deploy)
- Cuenta de Google Cloud Platform

### Paso 1: Clonar y configurar entorno

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno (Windows)
venv\Scripts\activate

# Activar entorno (Linux/Mac)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### Paso 2: Configurar variables de entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tus valores de GCP
```

### Paso 3: Ejecutar localmente

```bash
# Modo desarrollo con recarga automática
uvicorn app.main:app --reload

# La API estará disponible en: http://localhost:8000
# Documentación interactiva: http://localhost:8000/docs
```

## 📡 Endpoints

### `POST /upload-report`
Sube un PDF y procesa la información.

**Request:**
```bash
curl -X POST "http://localhost:8000/upload-report" \
  -F "file=@reporte_ultrasonido.pdf"
```

**Response:**
```json
{
  "report_id": "abc123",
  "message": "Reporte procesado exitosamente"
}
```

### `GET /reports/{report_id}`
Obtiene la información estructurada de un reporte.

**Response:**
```json
{
  "id": "abc123",
  "patient_name": "Max",
  "owner_name": "Juan Pérez",
  "veterinarian_name": "Dr. García",
  "diagnosis": "Cálculos renales en riñón izquierdo",
  "recommendations": "Dieta especial, control en 2 semanas",
  "image_urls": [
    "https://storage.googleapis.com/.../image1.jpg",
    "https://storage.googleapis.com/.../image2.jpg"
  ],
  "pdf_filename": "reporte_max.pdf",
  "upload_date": "2026-02-04T10:30:00"
}
```

## 🐳 Deploy a Cloud Run

### Paso 1: Build y push de imagen Docker

```bash
# Configurar proyecto GCP
gcloud config set project YOUR_PROJECT_ID

# Build de imagen
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/diagnovet-api

# Deploy a Cloud Run
gcloud run deploy diagnovet-api \
  --image gcr.io/YOUR_PROJECT_ID/diagnovet-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## 🔒 Seguridad

- Autenticación mediante API Keys (próximamente)
- Validación de tipos de archivo
- Rate limiting en endpoints
- Variables sensibles en variables de entorno

## 🧪 Testing

```bash
# Ejecutar tests (TODO)
pytest

# Ver cobertura
pytest --cov=app
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
- Validación automática de datos con Pydantic
- Documentación interactiva automática (Swagger)
- Alto rendimiento (async/await)
- Fácil de testear

### ¿Por qué Cloud Run?
- Escalabilidad automática
- Pago por uso (solo cuando hay requests)
- No requiere gestión de servidores
- Soporta contenedores Docker

### ¿Por qué Firestore?
- NoSQL flexible (ideal para datos semi-estructurados)
- Consultas en tiempo real
- Escalabilidad automática
- Integración nativa con GCP

### ¿Por qué Document AI?
- OCR avanzado con ML
- Extracción de entidades específicas
- Soporta documentos médicos complejos
- Mejor precisión que OCR tradicional

## 📝 TODO / Mejoras Futuras

- [ ] Autenticación con API Keys
- [ ] Rate limiting
- [ ] Tests automatizados
- [ ] CI/CD con GitHub Actions
- [ ] Monitoreo con Cloud Logging
- [ ] Webhooks para notificaciones
- [ ] Soporte para múltiples idiomas

## 👤 Autor

**Yeison** - Backend Engineer Challenge para DiagnoVET

## 📄 Licencia

Este proyecto es parte de un challenge técnico.
