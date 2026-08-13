import os
from PIL import Image
from src.modelos.constantes import EXTENSIONES_IMAGEN

import cv2
import numpy as np

class ProcesadorImagen:
    def obtener_resolucion(self, imagen):
        try:
            if not os.path.exists(imagen.ruta_completa):
                imagen.resolucion = "0x0"
                imagen.mensaje_error = f"Error el Archivo {imagen.nombre_completo} No existe"
                
                return imagen.resolucion
            
            with Image.open(imagen.ruta_completa) as img:
                ancho ,alto = img.size
                imagen.resolucion = f"{ancho}x{alto}"
                return imagen.resolucion
                
        except Exception as e:
            imagen.es_valida = False
            imagen.mensaje_error = f"Error al obtener resolución {e}"
            imagen.resolucion = "0x0"
            return imagen.resolucion
    
    def calcular_hash(self, imagen, tamaño_hash=32):
        try:
            
            if imagen.extension.lower() not in EXTENSIONES_IMAGEN:
                imagen.es_valida = False
                imagen.mensaje_error = f"Extensión no soportada: {imagen.extension}"
                imagen.hash = None
                return None
            
            img = Image.open(imagen.ruta_completa)
            img = img.resize((tamaño_hash, tamaño_hash), Image.Resampling.LANCZOS)
            img = img.convert('L')
            
            pixels = np.array(img, dtype=np.float32)
            dct = cv2.dct(pixels)
            dct_8x8 = dct[:8, :8]
            mediana = np.median(dct_8x8[1: ,:])
            
            hash_bits = []
            for y in range(8):
                for x in range(8):
                    hash_bits.append(1 if dct_8x8[y, x] > mediana else 0)
            
            hash_binario = ''.join(str(bit) for bit in hash_bits)
            imagen.hash = hex(int(hash_binario, 2))[2:].zfill(16)
            
            return imagen.hash
            
        except Exception as e:
            imagen.es_valida = False
            imagen.mensaje_error = f"Error al calcular hash: {e}"
            imagen.hash = None
            return None