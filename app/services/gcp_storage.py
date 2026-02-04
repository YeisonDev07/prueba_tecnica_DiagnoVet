"""
Servicio para interactuar con Google Cloud Storage.
Maneja la subida y descarga de archivos (imágenes).
"""
from typing import List
import os


class GCPStorageService:
    """
    Servicio para manejar Google Cloud Storage.
    
    Cloud Storage es como "Google Drive para aplicaciones".
    Aquí guardaremos las imágenes extraídas de los PDFs.
    
    TODO FASE 2: Implementar conexión real con GCP
    """
    
    def __init__(self, bucket_name: str = "diagnovet-reports-images"):
        """
        Inicializa el servicio de Storage.
        
        Args:
            bucket_name: Nombre del "contenedor" donde guardaremos archivos
        """
        self.bucket_name = bucket_name
        # TODO FASE 2: Inicializar cliente de Storage
        # from google.cloud import storage
        # self.client = storage.Client()
        # self.bucket = self.client.bucket(bucket_name)
    
    def upload_image(self, local_path: str, destination_blob_name: str) -> str:
        """
        Sube una imagen a Cloud Storage.
        
        Args:
            local_path: Ruta local de la imagen (ej: "./extracted_images/abc123_image_1.jpg")
            destination_blob_name: Nombre que tendrá en la nube (ej: "reports/abc123/image_1.jpg")
            
        Returns:
            str: URL pública de la imagen subida
        """
        # TODO FASE 2: Implementar subida real
        """
        blob = self.bucket.blob(destination_blob_name)
        blob.upload_from_filename(local_path)
        
        # Hacer el archivo público (para este challenge, las imágenes serán públicas)
        blob.make_public()
        
        return blob.public_url
        """
        
        # Por ahora, simulamos la URL
        return f"https://storage.googleapis.com/{self.bucket_name}/{destination_blob_name}"
    
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
        # TODO FASE 2: Implementar eliminación
        """
        blob = self.bucket.blob(blob_name)
        blob.delete()
        return True
        """
        return False
