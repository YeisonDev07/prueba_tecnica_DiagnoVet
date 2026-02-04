"""
Servicio para interactuar con Google Cloud Storage.
Maneja la subida y descarga de archivos (imágenes).
"""
from typing import List
import os
from google.cloud import storage


class GCPStorageService:
    """
    Servicio para manejar Google Cloud Storage.
    
    Cloud Storage es como "Google Drive para aplicaciones".
    Aquí guardaremos las imágenes extraídas de los PDFs.
    """
    
    def __init__(self, bucket_name: str = "diagnovet-reports-images", project_id: str = None):
        """
        Inicializa el servicio de Storage.
        
        Args:
            bucket_name: Nombre del "contenedor" donde guardaremos archivos
            project_id: ID del proyecto de GCP
        """
        self.bucket_name = bucket_name
        
        # Inicializar cliente de Storage con el project_id explícito
        self.client = storage.Client(project=project_id)
        self.bucket = self.client.bucket(bucket_name)
        
        print(f"✅ Cloud Storage inicializado: bucket '{bucket_name}' en proyecto '{project_id}'")
    
    def upload_image(self, local_path: str, destination_blob_name: str) -> str:
        """
        Sube una imagen a Cloud Storage.
        
        Args:
            local_path: Ruta local de la imagen (ej: "./extracted_images/abc123_image_1.jpg")
            destination_blob_name: Nombre que tendrá en la nube (ej: "reports/abc123/image_1.jpg")
            
        Returns:
            str: URL pública de la imagen subida
        """
        # Crear el blob (objeto en Cloud Storage)
        blob = self.bucket.blob(destination_blob_name)
        
        # Subir el archivo
        blob.upload_from_filename(local_path)
        
        # No llamamos make_public() porque el bucket tiene Uniform Access habilitado
        # La URL pública funciona si el bucket está configurado como público
        
        print(f"  ☁️  Imagen subida: {destination_blob_name}")
        
        return blob.public_url
    
    def upload_multiple_images(self, image_paths: List[str], report_id: str) -> List[str]:
        """
        Sube múltiples imágenes de un reporte.
        
        Args:
            image_paths: Lista de rutas locales de imágenes
            report_id: ID del reporte (para organizar en carpetas)
            
        Returns:
            List[str]: Lista de URLs públicas de las imágenes
        """
        image_urls = []
        
        for idx, image_path in enumerate(image_paths):
            # Crear nombre en la nube: reports/{report_id}/image_1.jpg
            filename = os.path.basename(image_path)
            destination = f"reports/{report_id}/{filename}"
            
            # Subir imagen
            url = self.upload_image(image_path, destination)
            image_urls.append(url)
        
        return image_urls
    
    def delete_image(self, blob_name: str) -> bool:
        """
        Elimina una imagen de Cloud Storage.
        
        Args:
            blob_name: Nombre del archivo en la nube
            
        Returns:
            bool: True si se eliminó correctamente
        """
        try:
            blob = self.bucket.blob(blob_name)
            blob.delete()
            print(f"  🗑️  Imagen eliminada: {blob_name}")
            return True
        except Exception as e:
            print(f"  ⚠️  Error eliminando imagen: {e}")
            return False
