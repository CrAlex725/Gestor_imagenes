from src.modelos.imagen import Imagen
import os

class ProcesadorCarpetas:
    def escanear(self, carpeta_imagen):
        print(f"Escaneando: {carpeta_imagen.ruta_base}")
        
        for carpeta, sub_carpetas, archivos in os.walk(carpeta_imagen.ruta_base):
            for archivo in archivos:
                carpeta_imagen.estadisticas['total_archivos'] +=1
                ruta_completa = os.path.join(carpeta, archivo)
                extension = os.path.splitext(archivo)[1].lower()
                
                if extension in carpeta_imagen.extensiones_validas:
                    imagen = Imagen(ruta_completa, carpeta_imagen.ruta_base)
                    carpeta_imagen.imagenes.append(imagen)
                    carpeta_imagen.estadisticas['imagenes_encontradas'] +=1
                    print(f"Imagen Encontrada: {archivo}")
                else:
                    carpeta_imagen.estadisticas['archivos_saltados'] +=1
                    print(f"Saltando: {archivo} ({extension})")
        
        print(f"\nResumen del escaneo")
        print(f"    - Total archivos: {carpeta_imagen.estadisticas['total_archivos']}")
        print(f"    - Imagenes: {carpeta_imagen.estadisticas['imagenes_encontradas']}")
        print(f"    - Saltados: {carpeta_imagen.estadisticas['archivos_saltados']}")
        
        return carpeta_imagen.imagenes