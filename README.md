# 📸 Gestor de Imágenes Duplicadas - Versión 0

> **Estado:** ⚠️ Versión inicial funcional pero monolítica (todo en un solo archivo).  
> **Propósito:** Esta versión documenta el punto de partida del proyecto, demostrando la lógica funcional antes de la refactorización.

---

## 🎯 ¿Qué hace esta herramienta?

Escanea una carpeta de imágenes, identifica duplicados mediante **hash perceptual (DCT)**, y clasifica automáticamente qué archivos conservar y cuáles eliminar según criterios de:

- **Resolución** (prioriza la más alta)
- **Tamaño en disco** (prioriza el más pequeño)
- **Fecha de creación** (prioriza la más antigua)

Además, asigna **etiquetas** y **ubicaciones** basadas en la estructura de carpetas, y exporta un **JSON** con el análisis completo.

---

## 🚀 Instalación y Uso

### 1. Requisitos previos
- Python 3.8 o superior
- Git (opcional, para clonar)

### 2. Clonar o descargar
```bash
git clone https://github.com/CrAlex725/Gestor_imagenes.git 
cd gestor-imagenes