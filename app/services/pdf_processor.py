"""
Servicio para procesar PDFs.
Extrae texto e imágenes de archivos PDF.
"""
import os
from typing import List, Dict
from PyPDF2 import PdfReader
from PIL import Image
import io


class PDFProcessor:
    """
    Maneja la extracción de información de PDFs.
    
    Fase 1 (Local): Usa PyPDF2 para extracción básica
    Fase 2 (GCP): Integrará Document AI para extracción avanzada
    """
    
    def __init__(self):
        """Inicializa el procesador de PDFs."""
        self.output_dir = "extracted_images"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def extract_text(self, pdf_path: str) -> str:
        """
        Extrae todo el texto de un PDF.
        
        Args:
            pdf_path: Ruta al archivo PDF
            
        Returns:
            str: Texto completo del PDF
        """
        try:
            reader = PdfReader(pdf_path)
            text = ""
            
            # Iterar por cada página y extraer texto
            for page_num, page in enumerate(reader.pages):
                page_text = page.extract_text()
                text += f"\n--- Página {page_num + 1} ---\n{page_text}"
            
            return text
        
        except Exception as e:
            print(f"❌ Error extrayendo texto del PDF: {e}")
            return ""
    
    def extract_images(self, pdf_path: str, report_id: str) -> List[str]:
        """
        Extrae imágenes de un PDF.
        
        Args:
            pdf_path: Ruta al archivo PDF
            report_id: ID del reporte (para nombrar las imágenes)
            
        Returns:
            List[str]: Lista de rutas a las imágenes extraídas
        """
        try:
            reader = PdfReader(pdf_path)
            image_paths = []
            image_counter = 0
            
            # Iterar por cada página
            for page_num, page in enumerate(reader.pages):
                # Intentar extraer imágenes de la página
                if '/XObject' in page['/Resources']:
                    x_objects = page['/Resources']['/XObject'].get_object()
                    
                    for obj_name in x_objects:
                        obj = x_objects[obj_name]
                        
                        # Verificar si es una imagen
                        if obj['/Subtype'] == '/Image':
                            try:
                                # Extraer datos de la imagen
                                size = (obj['/Width'], obj['/Height'])
                                data = obj.get_data()
                                
                                # Determinar formato
                                if '/Filter' in obj:
                                    filter_type = obj['/Filter']
                                    
                                    # Imágenes JPEG
                                    if filter_type == '/DCTDecode':
                                        image_counter += 1
                                        img_filename = f"{report_id}_image_{image_counter}.jpg"
                                        img_path = os.path.join(self.output_dir, img_filename)
                                        
                                        with open(img_path, "wb") as img_file:
                                            img_file.write(data)
                                        
                                        image_paths.append(img_path)
                                        print(f"  ✅ Imagen extraída: {img_filename}")
                                    
                                    # Otras imágenes (PNG, etc.)
                                    elif filter_type in ['/FlateDecode', '/JPXDecode']:
                                        image_counter += 1
                                        img_filename = f"{report_id}_image_{image_counter}.png"
                                        img_path = os.path.join(self.output_dir, img_filename)
                                        
                                        # Convertir a imagen PIL y guardar
                                        img = Image.frombytes('RGB', size, data)
                                        img.save(img_path)
                                        
                                        image_paths.append(img_path)
                                        print(f"  ✅ Imagen extraída: {img_filename}")
                            
                            except Exception as img_error:
                                print(f"  ⚠️  Error extrayendo una imagen: {img_error}")
                                continue
            
            return image_paths
        
        except Exception as e:
            print(f"❌ Error extrayendo imágenes del PDF: {e}")
            return []
    
    def extract_fields_with_document_ai(
        self, 
        pdf_path: str, 
        project_id: str, 
        location: str, 
        processor_id: str
    ) -> Dict[str, str]:
        """
        Extrae campos específicos usando Google Document AI OCR Processor.
        
        Args:
            pdf_path: Ruta al archivo PDF
            project_id: ID del proyecto de GCP
            location: Región del procesador (us, eu)
            processor_id: ID del procesador de Document AI
            
        Returns:
            Dict con los campos extraídos: patient_name, owner_name, etc.
        """
        try:
            from google.cloud import documentai_v1 as documentai
            
            # Inicializar cliente de Document AI
            opts = {"api_endpoint": f"{location}-documentai.googleapis.com"}
            client = documentai.DocumentProcessorServiceClient(client_options=opts)
            
            # Construir el nombre completo del procesador
            processor_name = client.processor_path(project_id, location, processor_id)
            
            # Leer el contenido del PDF
            with open(pdf_path, "rb") as pdf_file:
                pdf_content = pdf_file.read()
            
            # Crear la solicitud de procesamiento
            raw_document = documentai.RawDocument(
                content=pdf_content,
                mime_type="application/pdf"
            )
            
            request = documentai.ProcessRequest(
                name=processor_name,
                raw_document=raw_document
            )
            
            # Procesar el documento
            print(f"🤖 Procesando documento con Document AI OCR...")
            result = client.process_document(request=request)
            document = result.document
            
            # Extraer el texto completo
            full_text = document.text
            print(f"📄 Texto extraído por Document AI: {len(full_text)} caracteres")
            
            # Como el Custom Extractor no tiene esquema configurado,
            # vamos a extraer campos usando el texto con regex
            extracted_fields = self._extract_fields_from_text(full_text)
            
            # Debug: mostrar lo que se extrajo
            for field, value in extracted_fields.items():
                if value:
                    print(f"  ✅ {field}: {value[:100]}...")  # Primeros 100 chars
                else:
                    print(f"  ⚠️  {field}: No detectado")
            
            return extracted_fields
            
        except Exception as e:
            print(f"❌ Error procesando con Document AI: {e}")
            import traceback
            traceback.print_exc()
            # En caso de error, retornar campos vacíos
            return {
                "patient_name": None,
                "owner_name": None,
                "veterinarian_name": None,
                "diagnosis": None,
                "recommendations": None
            }
    
    def _extract_fields_from_text(self, text: str) -> Dict[str, str]:
        """
        Extrae campos específicos del texto usando patrones de regex.
        
        Args:
            text: Texto completo extraído del PDF
            
        Returns:
            Dict con los campos extraídos
        """
        import re
        
        fields = {
            "patient_name": None,
            "owner_name": None,
            "veterinarian_name": None,
            "diagnosis": None,
            "recommendations": None
        }
        
        # Patrones para buscar (case insensitive)
        patterns = {
            "patient_name": [
                r"paciente[:\s]+([A-Za-zÁÉÍÓÚáéíóúñÑ\s]+?)(?:\s+Propietario|Tutor|Raza|Especie|Edad|Sexo|\n)",
                r"nombre\s+(?:del\s+)?paciente[:\s]+([A-Za-zÁÉÍÓÚáéíóúñÑ\s]+?)(?:\s+Raza|Especie|Edad|\n)",
                r"patient[:\s]+([A-Za-zÁÉÍÓÚáéíóúñÑ\s]+?)(?:\s+Owner|Breed|Species|Age|\n)",
            ],
            "owner_name": [
                r"propietario[:\s]+([A-Za-zÁÉÍÓÚáéíóúñÑ\s]+?)(?:\s+Especie|Raza|Tel|Dirección|Teléfono|Sexo|Edad|\n)",
                r"tutor[:\s]+([A-Za-zÁÉÍÓÚáéíóúñÑ\s]+?)(?:\s+Raza|Tel|Dirección|Teléfono|\n)",
                r"dueño[:\s]+([A-Za-zÁÉÍÓÚáéíóúñÑ\s]+?)(?:\s+Tel|Dirección|\n)",
                r"owner[:\s]+([A-Za-zÁÉÍÓÚáéíóúñÑ\s]+?)(?:\s+Species|Phone|Address|\n)",
            ],
            "veterinarian_name": [
                r"referido\s+por[:\s]+([A-Za-zÁÉÍÓÚáéíóúñÑ\s\.]+?)(?:\n|\s+ANTECEDENTES)",
                r"derivante[:\s]+([A-Za-zÁÉÍÓÚáéíóúñÑ\s\.]+?)(?:\n|Solicitud)",
                r"(?:médico\s+)?veterinario[:\s]+([A-Za-zÁÉÍÓÚáéíóúñÑ\s\.]+?)(?:\s+Cédula|Fecha|Tel|\n)",
                r"médico[:\s]+([A-Za-zÁÉÍÓÚáéíóúñÑ\s\.]+?)(?:\s+Cédula|Fecha|\n)",
                r"doctor[:\s]+([A-Za-zÁÉÍÓÚáéíóúñÑ\s\.]+?)(?:\s+License|Date|\n)",
                r"MVZ[:\s\.]+([A-Za-zÁÉÍÓÚáéíóúñÑ\s\.]+?)(?:\s+Cédula|Fecha|\n)",
                r"elaboró[:\s]+([A-Za-zÁÉÍÓÚáéíóúñÑ\s\.]+?)(?:\s+Cédula|Fecha|\n)",
            ],
            "diagnosis": [
                r"(?:hallazgo|hallazgos)[s\s]*(?:bidimensional|radiográfico)?[:\s]*\n*(.{20,1500}?)(?:\n\s*CONCLUS|\n\s*©|\n\s*DiagnoVet|INDICACIONES|RECOMENDACIONES|$)",
                r"se\s+observa[:\s]*(.{20,1500}?)(?:\n\s*©|\n\s*DiagnoVet|\n\s*CONCLUS|\n\s*INDICACIONES|$)",
                r"diagnóstico[:\s]*(.{20,800}?)(?:\n\s*Recomendación|\n\s*Tratamiento|\n\s*Observación|$)",
                r"impresión\s+diagnóstica[:\s]*(.{20,800}?)(?:\n\s*Recomendación|\n\s*Tratamiento|$)",
                r"diagnosis[:\s]*(.{20,800}?)(?:\n\s*Recommendation|\n\s*Treatment|$)",
                r"conclusión[:\s]*(.{20,800}?)(?:\n\s*Recomendación|\n\s*INDICACIONES|$)",
            ],
            "recommendations": [
                r"(?:indicaciones|recomendaciones)[:\s]*(.{20,1000}?)(?:\n\s*©|\n\s*DiagnoVet|\n\s*Firma|\n\s*Elaboró|\n\s*M\.V\.|$)",
                r"recomendación(?:es)?[:\s]*(.{20,800}?)(?:\n\s*Firma|\n\s*Fecha\s+de\s+emisión|\n\s*Elaboró|$)",
                r"tratamiento[:\s]*(.{20,800}?)(?:\n\s*Firma|\n\s*Fecha|$)",
                r"recommendation(?:s)?[:\s]*(.{20,800}?)(?:\n\s*Signature|\n\s*Date|$)",
                r"conclusión[:\s]*(.{20,800}?)(?:\n\s*Indicaciones|\n\s*Recomendación|\n\s*Firma|$)",
            ],
        }
        
        # Buscar cada campo con sus patrones
        for field, field_patterns in patterns.items():
            for pattern in field_patterns:
                match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
                if match:
                    value = match.group(1).strip()
                    # Limpiar el valor (múltiples espacios y saltos de línea)
                    value = re.sub(r'\s+', ' ', value)
                    value = value.strip()
                    value = value[:500]  # Limitar longitud
                    
                    if len(value) > 2:  # Solo si tiene contenido válido
                        fields[field] = value
                        break  # Ya encontramos este campo, pasar al siguiente
        
        return fields
