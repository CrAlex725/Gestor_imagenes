class ListaDuplicados:
    def __init__(self):
        self.grupos_hash = {}
        
    def obtener_duplicados(self):
        return {hash: lista for hash, lista in self.grupos_hash.items() if len(lista) > 1}
    
    def obtener_unicos(self):
        return {hash: lista for hash, lista in self.grupos_hash.items() if len(lista) == 1}