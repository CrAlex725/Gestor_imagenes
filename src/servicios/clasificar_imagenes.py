class Clasificar:
    def __init__(self, lista_duplicados, gestor_duplicados):
        self.gestor_duplicados = gestor_duplicados
        self.lista_duplicados = lista_duplicados
        
    def clasificarImagenes(self):
        imagenes = self.lista_duplicados.grupos_hash
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
        