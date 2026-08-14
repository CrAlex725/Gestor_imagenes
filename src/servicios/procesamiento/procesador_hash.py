class ProcesadorHash:
    def procesar_una(self, imagen, procesador_imagen, configuracion_hash):
        """
        Procesa UNA sola imagen llamando a su método
        """
        configuracion_hash.estadisticas['procesadas'] += 1
        
        resultado = procesador_imagen.calcular_hash(imagen, configuracion_hash.tamaño_hash)
        
        if resultado:
            configuracion_hash.estadisticas['exitosas'] += 1
        else:
            configuracion_hash.estadisticas['fallidas'] += 1
            configuracion_hash.estadisticas['errores'].append({
                'imagen': imagen.nombre,
                'error': imagen.mensaje_error
            })
        
        return resultado
    
    def procesar_lote(self, imagenes, procesador_imagen, configuracion_hash):
        """
        Procesa un lote de imágenes
        """
        print(f"\n🔄 Procesando {len(imagenes)} imágenes con {configuracion_hash.algoritmo}...")
        
        # Reiniciar estadísticas
        configuracion_hash.reset_estadisticas()
        
        for i, imagen in enumerate(imagenes, 1):
            print(f"   [{i}/{len(imagenes)}] {imagen.nombre}", end="")
            
            resultado = self.procesar_una(imagen, procesador_imagen, configuracion_hash)
            
            if resultado:
                print(f" ✅ Hash: {resultado[:8]}...")
            else:
                print(f" ❌ {imagen.mensaje_error}")
        
        print(f"\n📊 Resumen del procesamiento:")
        print(f"   - Procesadas: {configuracion_hash.estadisticas['procesadas']}")
        print(f"   - Exitosas: {configuracion_hash.estadisticas['exitosas']}")
        print(f"   - Fallidas: {configuracion_hash.estadisticas['fallidas']}")
        
        if configuracion_hash.estadisticas['errores']:
            print(f"   - Errores: {len(configuracion_hash.estadisticas['errores'])}")
            for error in configuracion_hash.estadisticas['errores'][:3]:  # Mostrar primeros 3
                print(f"      • {error['imagen']}: {error['error']}")
        
        return configuracion_hash.estadisticas