"""
Servicio para interactuar con Firestore (base de datos).
Guarda y consulta la información de los reportes.
"""
from typing import Optional, List, Dict
from datetime import datetime
from google.cloud import firestore


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
    """
    
    def __init__(self, project_id: str = None):
        """
        Inicializa el servicio de Firestore.
        
        Args:
            project_id: ID del proyecto de GCP
        """
        # Inicializar cliente de Firestore
        self.db = firestore.Client(project=project_id)
        self.collection_name = "reports"
        
        print(f"✅ Firestore inicializado: colección '{self.collection_name}' en proyecto '{project_id}'")
    
    def save_report(self, report_data: Dict) -> str:
        """
        Guarda un reporte en Firestore.
        
        Args:
            report_data: Diccionario con los datos del reporte
            
        Returns:
            str: ID del documento creado
        """
        # Convertir datetime a timestamp si existe
        if 'upload_date' in report_data and isinstance(report_data['upload_date'], datetime):
            report_data['upload_date'] = report_data['upload_date']
        
        # Crear documento en Firestore con el ID del reporte
        doc_ref = self.db.collection(self.collection_name).document(report_data['id'])
        doc_ref.set(report_data)
        
        print(f"💾 Reporte guardado en Firestore: {report_data['id']}")
        return report_data['id']
    
    def get_report(self, report_id: str) -> Optional[Dict]:
        """
        Obtiene un reporte por su ID.
        
        Args:
            report_id: ID del reporte a buscar
            
        Returns:
            Dict con los datos del reporte, o None si no existe
        """
        doc_ref = self.db.collection(self.collection_name).document(report_id)
        doc = doc_ref.get()
        
        if doc.exists:
            print(f"🔍 Reporte encontrado en Firestore: {report_id}")
            return doc.to_dict()
        
        print(f"⚠️  Reporte no encontrado: {report_id}")
        return None
    
    def list_reports(self, limit: int = 100) -> List[Dict]:
        """
        Lista todos los reportes.
        
        Args:
            limit: Número máximo de reportes a retornar
            
        Returns:
            Lista de diccionarios con los reportes
        """
        docs = self.db.collection(self.collection_name).limit(limit).stream()
        reports = [doc.to_dict() for doc in docs]
        
        print(f"📋 Listando {len(reports)} reportes desde Firestore")
        return reports
    
    def update_report(self, report_id: str, updates: Dict) -> bool:
        """
        Actualiza campos de un reporte existente.
        
        Args:
            report_id: ID del reporte
            updates: Diccionario con los campos a actualizar
            
        Returns:
            bool: True si se actualizó correctamente
        """
        try:
            doc_ref = self.db.collection(self.collection_name).document(report_id)
            doc_ref.update(updates)
            print(f"✏️  Reporte actualizado: {report_id}")
            return True
        except Exception as e:
            print(f"❌ Error actualizando reporte: {e}")
            return False
    
    def delete_report(self, report_id: str) -> bool:
        """
        Elimina un reporte.
        
        Args:
            report_id: ID del reporte a eliminar
            
        Returns:
            bool: True si se eliminó correctamente
        """
        try:
            doc_ref = self.db.collection(self.collection_name).document(report_id)
            doc_ref.delete()
            print(f"🗑️  Reporte eliminado: {report_id}")
            return True
        except Exception as e:
            print(f"❌ Error eliminando reporte: {e}")
            return False