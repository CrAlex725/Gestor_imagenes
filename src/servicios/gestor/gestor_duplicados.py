class GestorDuplicados:
    def agrupar_hash(self, imagenes, lista_duplicados):
        for imagen in imagenes:
            if imagen.hash is None:
                continue
            
            if imagen.hash not in lista_duplicados.grupos_hash:
                lista_duplicados.grupos_hash[imagen.hash] = []
                
            lista_duplicados.grupos_hash[imagen.hash].append(imagen)
                
        return lista_duplicados.grupos_hash
    
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