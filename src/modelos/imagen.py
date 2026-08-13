from datetime import datetime
import os

class Imagen:
    def __init__(self, ruta_completa, ruta_base):
        
        self.ruta_completa = ruta_completa
        self.ruta_base = ruta_base
        
        self.nombre_completo = os.path.basename(ruta_completa)
        self.nombre = os.path.splitext(self.nombre_completo)[0]
        self.extension = os.path.splitext(self.nombre_completo)[1]
        
        self.tamaño = os.path.getsize(ruta_completa)
        
        self.fecha_creacion = datetime.fromtimestamp(
            os.path.getctime(ruta_completa)
        ).strftime('%Y-%m-%d %H:%M:%S')
        self.fecha_modificacion = datetime.fromtimestamp(
            os.path.getmtime(ruta_completa)
        ).strftime('%Y-%m-%d %H:%M:%S')
        
        self.ruta_relativa = os.path.relpath(ruta_completa, ruta_base)
        
        self.resolucion = None
        self.hash = None
        self.etiquetas = []
        self.estado = "Pendiente"
        self.ubicaciones = []
        
        self.es_valida = True
        self.mensaje_error = None