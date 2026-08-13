class SerializadorImagen:
    def to_dict(self, imagen):
        return {
            "nombre": imagen.nombre,
            "extension": imagen.extension,
            "hash": imagen.hash,
            "estado": imagen.estado,
            "resolucion": imagen.resolucion,
            "tamaño": imagen.tamaño,
            "ruta": imagen.ruta_relativa,
            "ubicaciones": imagen.ubicaciones,
            "etiquetas": imagen.etiquetas,
            "fecha_creacion": imagen.fecha_creacion,
            "fecha_modificacion": imagen.fecha_modificacion
        }
        
