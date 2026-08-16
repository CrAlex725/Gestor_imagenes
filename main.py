from src.servicios.procesamiento.procesador_imagen import ProcesadorImagen
from src.utilidades.serializador_imagen import SerializadorImagen

from src.modelos.carpeta_imagenes import CarpetaImagenes
from src.servicios.procesamiento.procesador_carpetas import ProcesadorCarpetas

from src.modelos.configuracion_hash import ConfiguracionHash
from src.servicios.procesamiento.procesador_hash import ProcesadorHash

from src.modelos.lista_duplicados import ListaDuplicados
from src.servicios.gestor.gestor_duplicados import GestorDuplicados

from src.servicios.gestor.asignador_etiquetas import AsignadorEtiquetas

from src.servicios.clasificar_imagenes import Clasificar

from src.servicios.exportar_archivo_json import ExportarArchivoJson

if __name__ == "__main__":
    # 1. Crear el gestor de carpeta/ Escanear
    carpeta = CarpetaImagenes(f"C:/Users/crale/Desktop/USB/-Arte/Animatic")
    procesar_carpeta = ProcesadorCarpetas()
    imagenes = procesar_carpeta.escanear(carpeta)
    
    # 2. Procesar
    procesador = ProcesadorHash()
    procesador_imagen = ProcesadorImagen()
    configuracion_hash = ConfiguracionHash(procesador_imagen)
    for imagen in imagenes:
        procesador.procesar_una(imagen, procesador_imagen, configuracion_hash)
        
    lista_duplic = ListaDuplicados()
    gestor = GestorDuplicados()
    
    gestor.agrupar_hash(imagenes, lista_duplic)
    
    # ---
    
    asignador = AsignadorEtiquetas()
    asignador.asignar_ubicaciones_y_etiquetas(imagenes, lista_duplic)
    
    clasificador = Clasificar(lista_duplic, gestor)
    clasificador.clasificarImagenes()
    
    serializador = SerializadorImagen()
    export = ExportarArchivoJson(lista_duplic.grupos_hash, serializador)
    
    resultados = export.exportar("resultados_finales.json")
    