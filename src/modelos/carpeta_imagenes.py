from src.modelos.constantes import EXTENSIONES_IMAGEN

class CarpetaImagenes:
    def __init__(self, ruta_base):
        self.ruta_base = ruta_base
        self.imagenes = []
        self.extensiones_validas = EXTENSIONES_IMAGEN
        self.estadisticas = {
            'total_archivos': 0,
            'imagenes_encontradas': 0,
            'archivos_saltados': 0
        }
    
    def obtener_imagenes_validas(self):
        
        return [img for img in self.imagenes if img.es_valida]
    
    def obtener_imagenes_invalidas(self):
        return [img for img in self.imagenes if not img.es_valida]