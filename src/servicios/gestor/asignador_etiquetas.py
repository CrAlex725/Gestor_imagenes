import os

class AsignadorEtiquetas:
    
    def asignar_ubicaciones_y_etiquetas(self, imagenes, lista_duplicados):
        """
        Asigna ubicaciones y etiquetas a todas las imágenes
        """
        # 1. Obtener los grupos de duplicados
        grupos = lista_duplicados.grupos_hash
        
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