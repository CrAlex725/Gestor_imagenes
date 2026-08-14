from src.modelos.imagen import Imagen
from src.modelos.constantes import EXTENSIONES_IMAGEN
from src.servicios.procesamiento.procesador_imagen import ProcesadorImagen
from src.utilidades.serializador_imagen import SerializadorImagen

from src.modelos.carpeta_imagenes import CarpetaImagenes
from src.servicios.procesamiento.procesador_carpetas import ProcesadorCarpetas

import os
import time
from datetime import datetime
import re
import json

import cv2
import numpy as np
from PIL import Image
import mimetypes

class ProcesadorHash:  # ← Nombre con mayúscula (convención Python)
    
    def __init__(self, tamaño_hash=32, algoritmo='dct'):
        self.tamaño_hash = tamaño_hash
        self.algoritmo = algoritmo
        self.extensiones_validas = EXTENSIONES_IMAGEN
        self.procesador_imagen = ProcesadorImagen()
        
        self.estadisticas = {
            'procesadas': 0,
            'exitosas': 0,
            'fallidas': 0,
            'errores': []
        }
    
    def procesar_una(self, imagen):
        """
        Procesa UNA sola imagen llamando a su método
        """
        self.estadisticas['procesadas'] += 1
        
        resultado = self.procesador_imagen.calcular_hash(imagen, self.tamaño_hash)
        
        if resultado:
            self.estadisticas['exitosas'] += 1
        else:
            self.estadisticas['fallidas'] += 1
            self.estadisticas['errores'].append({
                'imagen': imagen.nombre,
                'error': imagen.mensaje_error
            })
        
        return resultado
    
    def procesar_lote(self, imagenes):
        """
        Procesa un lote de imágenes
        """
        print(f"\n🔄 Procesando {len(imagenes)} imágenes con {self.algoritmo}...")
        
        # Reiniciar estadísticas
        self.reset_estadisticas()
        
        for i, imagen in enumerate(imagenes, 1):
            print(f"   [{i}/{len(imagenes)}] {imagen.nombre}", end="")
            
            resultado = self.procesar_una(imagen)
            
            if resultado:
                print(f" ✅ Hash: {resultado[:8]}...")
            else:
                print(f" ❌ {imagen.mensaje_error}")
        
        print(f"\n📊 Resumen del procesamiento:")
        print(f"   - Procesadas: {self.estadisticas['procesadas']}")
        print(f"   - Exitosas: {self.estadisticas['exitosas']}")
        print(f"   - Fallidas: {self.estadisticas['fallidas']}")
        
        if self.estadisticas['errores']:
            print(f"   - Errores: {len(self.estadisticas['errores'])}")
            for error in self.estadisticas['errores'][:3]:  # Mostrar primeros 3
                print(f"      • {error['imagen']}: {error['error']}")
        
        return self.estadisticas
    
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
    

class GestorDuplicados:
    def __init__(self):
        self.grupos_hash = {}
        
    def agrupar_hash(self, imagenes):
        for imagen in imagenes:
            if imagen.hash is None:
                continue
            
            if imagen.hash not in self.grupos_hash:
                self.grupos_hash[imagen.hash] = []
                
            self.grupos_hash[imagen.hash].append(imagen)
                
        return self.grupos_hash
    
    def agrupar_resolucion(self, imagenes):
        grupos = {}
        for imagen in imagenes:
            if imagen.resolucion is None:
                continue
            
            grupos.setdefault(imagen.resolucion, []).append(imagen)
            
        return grupos
        
    def agrupar_tamano(self, imagenes):
        grupos = {}
        for imagen in imagenes:
            if imagen.tamaño is None:
                continue
            
            grupos.setdefault(imagen.tamaño, []).append(imagen)
                
        return grupos
    
    def agrupar_fecha(self, imagenes):
        grupos = {}
        for imagen in imagenes:
            if imagen.fecha_creacion is None:
                continue
                
            grupos.setdefault(imagen.fecha_creacion, []).append(imagen)
                
        return grupos
    
    def obtener_duplicados(self):
        return {hash: lista for hash, lista in self.grupos_hash.items() if len(lista) > 1}
    
    def obtener_unicos(self):
        return {hash: lista for hash, lista in self.grupos_hash.items() if len(lista) == 1}
    

class AsignadorEtiquetas:
    
    def asignar_ubicaciones_y_etiquetas(self, imagenes, gestor_duplicados):
        """
        Asigna ubicaciones y etiquetas a todas las imágenes
        """
        # 1. Obtener los grupos de duplicados
        grupos = gestor_duplicados.grupos_hash
        
        # 2. Procesar cada grupo
        for hash_imagen, lista_imagenes in grupos.items():
            
            # 2.1. Si solo hay una imagen, procesarla individualmente
            if len(lista_imagenes) == 1:
                imagen = lista_imagenes[0]
                ubicaciones = self._extraer_ubicaciones(imagen.ruta_relativa)
                imagen.ubicaciones = ubicaciones
                
                etiquetas = ubicaciones.copy()
                if "-- " in imagen.nombre:
                    etiquetas.append("Favoritos")
                imagen.etiquetas = list(set(etiquetas))
                continue
            
            # 2.2. Si hay más de una imagen, recolectar TODAS las ubicaciones
            todas_ubicaciones = []
            es_favorito = False
            
            for imagen in lista_imagenes:
                # Extraer ubicaciones de esta imagen
                ubicaciones = self._extraer_ubicaciones(imagen.ruta_relativa)
                # Agregar a la lista de todas las ubicaciones
                for ubicacion in ubicaciones:
                    todas_ubicaciones.append(ubicacion)
                
                # Verificar si alguna imagen del grupo es favorito
                if "-- " in imagen.nombre:
                    es_favorito = True
            
            # 2.3. Limpiar duplicados en las ubicaciones
            todas_ubicaciones = list(dict.fromkeys(todas_ubicaciones))
            
            # 2.4. Extraer etiquetas desde todas las ubicaciones
            etiquetas = []
            for ubicacion in todas_ubicaciones:
                # Dividir la ubicación en partes
                partes = ubicacion.split(os.sep)
                for parte in partes:
                    if parte:  # Si no está vacío
                        etiquetas.append(parte)
            
            # 2.5. Limpiar duplicados en etiquetas
            etiquetas = list(dict.fromkeys(etiquetas))
            
            # 2.6. Si alguna imagen es favorito, agregar etiqueta
            if es_favorito:
                etiquetas.append("Favoritos")
            
            # 2.7. Asignar a TODAS las imágenes del grupo
            for imagen in lista_imagenes:
                imagen.ubicaciones = todas_ubicaciones
                imagen.etiquetas = etiquetas.copy()
    
    def _extraer_ubicaciones(self, ruta_relativa):
        """
        PRIVADO: Extrae las carpetas de una ruta relativa
        Ejemplo: "carpeta1/carpeta1.1/imagen.jpg" → ["carpeta1/carpeta1.1"]
        """
        # Eliminar el nombre del archivo
        partes = ruta_relativa.split(os.sep)
        
        # Eliminar el último elemento (el archivo)
        if partes:
            partes.pop()
        
        # Si no hay carpetas, devolver lista vacía
        if not partes:
            return []
        
        # Reconstruir la ruta de las carpetas
        # Ejemplo: ["carpeta1", "carpeta1.1"] → "carpeta1/carpeta1.1"
        return [os.sep.join(partes)]

class Clasificar:
    def __init__(self, gestor_duplicados):
        self.gestor_duplicados = gestor_duplicados
        
    def clasificarImagenes(self):
        imagenes = self.gestor_duplicados.grupos_hash
        for hash_image, lista_image in imagenes.items():
            if len(lista_image) == 1:
                lista_image[0].estado = "Conservar"
                continue
            
            for archivo in lista_image:
                archivo.estado = "Pendiente"
                
            pendientes = self.procesarResolusion(lista_image)
            
            if len(pendientes) > 1:
                pendientes = self.procesarTamaño(pendientes)
                
            if len(pendientes) > 1:
                pendientes = self.procesarFecha(pendientes)
                
            if len(pendientes) == 1:
                pendientes[0].estado = "Conservar"
                
            elif len(pendientes) > 1:
                pendientes.sort(key=lambda x: x.fecha_creacion)
                pendientes[0].estado = "Conservar"
                
                for archivo in pendientes[1: ]:
                    archivo.estado = "Eliminar"
                    
            for archivo in lista_image:
                if archivo not in pendientes and archivo.estado != "Conservar":
                    archivo.estado = "Eliminar"
    
    def procesarResolusion(self, lista_archivos):
        pendientes = [a for a in lista_archivos if a.estado == "Pendiente"]
        
        if len(pendientes) <= 1:
            return pendientes
        
        grupos_resolucion = self.gestor_duplicados.agrupar_resolucion(pendientes)
        
        if len(grupos_resolucion) <= 1:
            return pendientes
        
        # Encontrar la resolución más alta
        resolucion_maxima = None
        area_maxima = -1
        
        for resol, lista in grupos_resolucion.items():
            ancho, alto = map(int, resol.split('x'))
            area = ancho * alto
            if area > area_maxima:
                area_maxima = area
                resolucion_maxima = resol
                
        if resolucion_maxima is None:
            return pendientes
        
        # Marcar TODOS los que NO son de la resolución máxima como Eliminar
        archivos_max = grupos_resolucion[resolucion_maxima]
        
        if len(archivos_max) == 1:
            # Solo uno en resolución máxima → se convierte en Conservar
            archivos_max[0].estado = "Conservar"
            return []  # No hay pendientes
        else:
            # Múltiples en resolución máxima → todos siguen pendientes
            # Los demás se marcan como Eliminar
            for archivo in pendientes:
                if archivo not in archivos_max:
                    archivo.estado = "Eliminar"
            return archivos_max  # Solo los de resolución máxima siguen pendientes
        
    def procesarTamaño(self, lista_archivos):
        if len(lista_archivos) <= 1:
            return lista_archivos
        
        grupos_tamaño = self.gestor_duplicados.agrupar_tamano(lista_archivos)
        
        if len(grupos_tamaño) <= 1:
            return lista_archivos
        
        minimo_tamaño = min(grupos_tamaño.keys())
        archivos_min = grupos_tamaño[minimo_tamaño]
        
        for tamano, lista in grupos_tamaño.items():
            if tamano != minimo_tamaño:
                for archivo in lista:
                    if archivo.estado != "Conservar":
                        archivo.estado = "Eliminar"
                    
        if len(archivos_min) == 1:
            archivos_min[0].estado = 'Conservar'
            return []
        else:
            return archivos_min
        
    def procesarFecha(self, lista_archivos):
        if len(lista_archivos) <= 1:
            return lista_archivos
        
        grupos_fecha = self.gestor_duplicados.agrupar_fecha(lista_archivos)
        
        if len(grupos_fecha) <= 1:
            return lista_archivos
        
        fecha_antigua = min(grupos_fecha.keys())
        archivos_antiguos = grupos_fecha[fecha_antigua]
        
        for fecha, lista in grupos_fecha.items():
            if fecha != fecha_antigua:
                for archivo in lista:
                    if archivo.estado != "Conservar":
                        archivo.estado = "Eliminar"
                    
        if len(archivos_antiguos) == 1:
            archivos_antiguos[0].estado = "Conservar"
            return []
        else:
            return archivos_antiguos
        
class Exportar():
    def __init__(self, diccionario_agrupado):
        self.serializador = SerializadorImagen()
        self.datos_entrada = diccionario_agrupado
        self.resultados = None
        self.resumen = None
        
        if not isinstance(diccionario_agrupado, dict):
            raise TypeError("Los Datos deben ser un diccionario")
        
        for key, value in diccionario_agrupado.items():
            if not isinstance(value, list):
                raise TypeError(f"El valor para la clave {key} debe ser una lista")
            if value and not isinstance(value[0], Imagen):
                raise TypeError(f"Los elementos deben ser objetos de la clase Imagen")
    
    def crear_json(self):
        if not self.datos_entrada:
            print("No Hay Datos para propcesar")
            return None
        
        self.resultados = {
            "resumen": {
                "total_hashes": len(self.datos_entrada),
                "total_archivos": 0,
                "Conservados": 0,
                "Eliminados": 0,
                "Pendientes": 0
            },
            "archivos_por_hash": []
        }
        
        for hash_value, lista_imagenes in self.datos_entrada.items():
            grupo = {
                "hash": hash_value,
                "cantidad_archivos": len(lista_imagenes),
                "archivos": []
            }
            
            for imagen in lista_imagenes:
                self._actualizar_estadisticas(imagen)
                
                datos_imagen = self._crear_archivo_limpio(imagen)
                grupo["archivos"].append(datos_imagen)
                
            self.resultados["archivos_por_hash"].append(grupo)
            
        self.resumen = self.resultados["resumen"]
        
        return self.resultados
                
    def _actualizar_estadisticas(self, imagen):
        self.resultados["resumen"]["total_archivos"] +=1
        
        estado = imagen.estado if hasattr(imagen, 'estado') else 'No definido'
        
        if estado == 'Conservar':
            self.resultados["resumen"]["Conservados"] +=1
        elif estado == 'Eliminar':
            self.resultados["resumen"]["Eliminados"] +=1
        elif estado == 'Pendiente':
            self.resultados["resumen"]["Pendientes"] +=1
            
    def _crear_archivo_limpio(self, imagen):
        datos_base = self.serializador.to_dict(imagen)
        
        archivo_limpio = {
            "nombre": datos_base.get('nombre', ''),
            "extension": datos_base.get('extension', ''),
            "ruta_relativa": datos_base.get('ruta', ''),
            "ruta_origen": imagen.ruta_completa if hasattr(imagen, 'ruta_completa') else '',
            
            "resolucion": datos_base.get('resolucion', ''),
            "tamaño_bytes": datos_base.get('tamaño', 0),
            "tamaño_kb": round(datos_base.get('tamaño', 0) / 1024, 2),
            "tamaño_mb": round(datos_base.get('tamaño', 0) / (1024 * 1024), 2),
            "fecha_creacion": datos_base.get('fecha_creacion', ''),
            "fecha_modificacion": datos_base.get('fecha_modificacion', ''),
            "hash": datos_base.get('hash', ''),
            "estado": datos_base.get('estado', 'No definido'),
            "etiquetas": datos_base.get('etiquetas', []),
            "ubicaciones": datos_base.get('ubicaciones', [])
        }
        
        return archivo_limpio
            
    def guardar_json(self, ruta_salida="resultados.json"):
        if self.resultados is None:
            print("Error: Primero debe llamar a crear_json()")
            return False
        
        try:
            with open(ruta_salida, 'w', encoding='utf-8')as f:
                json.dump(self.resultados, f, indent=4, ensure_ascii=False)
                
            print(f"Resultados exportados a: {ruta_salida}")
            self._mostrar_resumen()
            return True
        
        except PermissionError:
            print(f"Error No tienes permisos para escribir en {ruta_salida}")
            return False
        except Exception as e:
            print(f"Error al guardar el archivo: {e}")
            return False
        
    def _mostrar_resumen(self):
        if self.resumen is None:
            print("No Hay resumen Disponible")
            return
        
        print(f"📊 Resumen:")
        print(f"   - Total archivos: {self.resumen['total_archivos']}")
        print(f"   - Conservados: {self.resumen['Conservados']}")
        print(f"   - Eliminados: {self.resumen['Eliminados']}")
        print(f"   - Pendientes: {self.resumen['Pendientes']}")
        print(f"   - Hashes únicos: {self.resumen['total_hashes']}")
        
    def exportar(self, ruta_salida="resultados.json"):
        self.crear_json()
        
        if self.resultados is None:
            print("Error: no se pudo crear la estructura JSON")
            return None
        
        exito = self.guardar_json(ruta_salida)
        
        if not exito:
            print("Error: no se pudo guardar el archivo")
            return None
        
        return self.resultados
        

if __name__ == "__main__":
    # 1. Crear el gestor de carpeta/ Escanear
    carpeta = CarpetaImagenes(f"C:/Users/crale/Desktop/USB/---")
    procesar_carpeta = ProcesadorCarpetas()
    imagenes = procesar_carpeta.escanear(carpeta)
    
    # 2. Procesar
    procesador = ProcesadorHash()
    for imagen in imagenes:
        procesador.procesar_una(imagen)
        
    gestor = GestorDuplicados()
    gestor.agrupar_hash(imagenes)
        
    asignador = AsignadorEtiquetas()
    asignador.asignar_ubicaciones_y_etiquetas(imagenes, gestor)
    
    clasificador = Clasificar(gestor)
    clasificador.clasificarImagenes()
    
    export = Exportar(gestor.grupos_hash)
    
    resultados = export.exportar("resultados_finales.json")
    