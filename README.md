# [Página web de RoboRescue UMA](https://www.roborescue.uma.es)

[![Deploy Status](https://github.com/RoboRescueUMA/roborescueuma.github.io/actions/workflows/publish.yaml/badge.svg)](https://github.com/RoboRescueUMA/roborescueuma.github.io/actions/workflows/publish.yaml)

## Sobre RoboRescue UMA
RoboRescue UMA es un equipo compuesto por estudiantes de diversos ámbitos de la Universidad de Málaga, unidos con un fin común: el desarrollo tecnológico-robótico de rescate. Este proyecto comenzó en 2019 con la intención de dar visibilidad a las posibles soluciones prácticas que podemos encontrar gracias a la robótica y la automatización.

## TODOs (tareas pendientes)
Las tareas pendientes, en orden de prioridad, son:
- [ ] Crear script de python para convertir la información de `authors.xlsx` (generado con `scripts/python/export_authors_to_excel.py`) a los archivos `_index.md` correspondientes en inglés y español
- [ ] Quitar o reemplazar placeholders
- [ ] Encuestar a los miembros para información actualizada, fotos y redes sociales
- [ ] Corregir bug donde el selector de idioma solo aparece en ciertas áreas
- [ ] Crear y documentar [LICENSE.md](LICENSE.md)
- [ ] Crear y documentar [Contributing.md](Contributing.md)
- [ ] Crear un archivo [copilot-instructions.md](https://docs.github.com/es/copilot/how-tos/configure-custom-instructions/add-repository-instructions) para GitHub Copilot
- [X] Renombrar carpetas en content/es/authors
- [X] Mejorar este README.md

## Información técnica
- Desarrollado utilizando [HugoBlox](https://hugoblox.com/), un generador de sitios estáticos basado en [Hugo](https://gohugo.io/)
- Tema: [Research Group](https://github.com/HugoBlox/theme-research-group)
- Al hacer un cambio en la rama `main`, se despliega automáticamente en Github Pages
- Se utiliza Google Analytics para seguimiento de visitas

## Diseño
- Diseño está inspirado en [clubcapra.com](https://clubcapra.com)

## Para contribuidores
- Documentación de HugoBlox: https://docs.hugoblox.com/
- El repositorio cuenta con un archivo [.editorconfig](.editorconfig) para mantener consistencia. Es recomendable instalar su [plugin](https://editorconfig.org/#download) en el IDE que se utilice.

## Scripts
En el directorio `scripts/` hay varios scripts útiles:
- `clone-authors.ps1` - Clona autores entre carpetas
- `optimize-images.ps1` - Optimiza imágenes del proyecto

### Scripts de Python
El subdirectorio `scripts/python/` contiene scripts de Python con su propio entorno virtual aislado:

- **`export_authors_to_excel.py`** - Exporta información de todos los autores del directorio `content/es/authors/` a un archivo Excel (`authors.xlsx`)
- **`setup_env.ps1`** - Gestor automático del entorno virtual Python

#### Uso del entorno Python:
```powershell
# Configuración inicial (solo la primera vez)
cd scripts\python
.\setup_env.ps1 setup

# Ejecutar script de exportación
.\setup_env.ps1 run

# Ver todos los comandos disponibles
.\setup_env.ps1 help
```

El entorno virtual garantiza que las dependencias estén aisladas del sistema global. Idealmente los scripts futuros se deben escribir en Python y guardar en este subdirectorio para mejor compatibilidad.

