from src.modelos.imagen import Imagen
import json

class ExportarArchivoJson():
    def __init__(self, diccionario_agrupado, serializador):
        self.serializador = serializador
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