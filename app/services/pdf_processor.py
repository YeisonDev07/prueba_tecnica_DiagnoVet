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
    
    def extract_fields_with_document_ai(self, pdf_path: str) -> Dict[str, str]:
        """
        Extrae campos específicos usando Google Document AI.
        
        TODO FASE 2: Implementar integración con Document AI
        
        Args:
            pdf_path: Ruta al archivo PDF
            
        Returns:
            Dict con los campos extraídos: patient_name, owner_name, etc.
        """
        # Por ahora retornamos un diccionario vacío
        # Lo implementaremos en la Fase 2 cuando configuremos GCP
        return {
            "patient_name": "",
            "owner_name": "",
            "veterinarian_name": "",
            "diagnosis": "",
            "recommendations": ""
        }
