from src.modelos.constantes import EXTENSIONES_IMAGEN

class ConfiguracionHash:  # ← Nombre con mayúscula (convención Python)
    
    def __init__(self, procesador_imagen, tamaño_hash=32, algoritmo='dct'):
        self.tamaño_hash = tamaño_hash
        self.algoritmo = algoritmo
        self.extensiones_validas = EXTENSIONES_IMAGEN
        self.procesador_imagen = procesador_imagen
        
        self.estadisticas = {
            'procesadas': 0,
            'exitosas': 0,
            'fallidas': 0,
            'errores': []
        }
    
    def reset_estadisticas(self):
        self.estadisticas = {
            'procesadas': 0,
            'exitosas': 0,
            'fallidas': 0,
            'errores': []
        }
    
    def obtener_validas(self, imagenes):
        """Filtra imágenes con hash válido"""
        return [img for img in imagenes if img.hash is not None and img.es_valida]
    
    def obtener_invalidas(self, imagenes):
        """Filtra imágenes sin hash válido"""
        return [img for img in imagenes if img.hash is None or not img.es_valida]
    