"""
Servicio para interactuar con Firestore (base de datos).
Guarda y consulta la información de los reportes.
"""
from typing import Optional, List, Dict
from datetime import datetime


class FirestoreService:
    """
    Servicio para manejar Firestore (base de datos NoSQL de Google).
    
    Firestore guarda datos como "documentos" (objetos JSON).
    Cada reporte será un documento en la colección "reports".
    
    Estructura:
    reports/
      └─ {report_id}/
           ├─ patient_name: "Max"
           ├─ owner_name: "Juan Pérez"
           ├─ diagnosis: "Cálculos renales..."
           ├─ image_urls: ["url1", "url2"]
           └─ upload_date: 2026-02-04T10:30:00
    
    TODO FASE 2: Implementar conexión real con GCP
    """
    
    def __init__(self):
        """Inicializa el servicio de Firestore."""
        # TODO FASE 2: Inicializar cliente de Firestore
        # from google.cloud import firestore
        # self.db = firestore.Client()
        self.collection_name = "reports"
    
    def save_report(self, report_data: Dict) -> str:
        """
        Guarda un reporte en Firestore.
        
        Args:
            report_data: Diccionario con los datos del reporte
            
        Returns:
            str: ID del documento creado
        """
        # TODO FASE 2: Implementar guardado real
        """
        doc_ref = self.db.collection(self.collection_name).document(report_data['id'])
        doc_ref.set(report_data)
        return report_data['id']
        """
        
        # Por ahora solo imprimimos
        print(f"💾 [SIMULADO] Guardando reporte: {report_data.get('id')}")
        return report_data.get('id', 'unknown')
    
    def get_report(self, report_id: str) -> Optional[Dict]:
        """
        Obtiene un reporte por su ID.
        
        Args:
            report_id: ID del reporte a buscar
            
        Returns:
            Dict con los datos del reporte, o None si no existe
        """
        # TODO FASE 2: Implementar consulta real
        """
        doc_ref = self.db.collection(self.collection_name).document(report_id)
        doc = doc_ref.get()
        
        if doc.exists:
            return doc.to_dict()
        return None
        """
        
        # Por ahora retornamos None
        print(f"🔍 [SIMULADO] Buscando reporte: {report_id}")
        return None
    
    def list_reports(self, limit: int = 100) -> List[Dict]:
        """
        Lista todos los reportes.
        
        Args:
            limit: Número máximo de reportes a retornar
            
        Returns:
            Lista de diccionarios con los reportes
        """
        # TODO FASE 2: Implementar listado real
        """
        docs = self.db.collection(self.collection_name).limit(limit).stream()
        return [doc.to_dict() for doc in docs]
        """
        
        print(f"📋 [SIMULADO] Listando reportes (límite: {limit})")
        return []
    
    def update_report(self, report_id: str, updates: Dict) -> bool:
        """
        Actualiza campos de un reporte existente.
        
        Args:
            report_id: ID del reporte
            updates: Diccionario con los campos a actualizar
            
        Returns:
            bool: True si se actualizó correctamente
        """
        # TODO FASE 2: Implementar actualización
        """
        doc_ref = self.db.collection(self.collection_name).document(report_id)
        doc_ref.update(updates)
        return True
        """
        return False
    
    def delete_report(self, report_id: str) -> bool:
        """
        Elimina un reporte.
        
        Args:
            report_id: ID del reporte a eliminar
            
        Returns:
            bool: True si se eliminó correctamente
        """
        # TODO FASE 2: Implementar eliminación
        """
        doc_ref = self.db.collection(self.collection_name).document(report_id)
        doc_ref.delete()
        return True
        """
        return False
