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

- Documentación de HugoBlox: <https://docs.hugoblox.com/>
- El repositorio cuenta con un archivo [.editorconfig](.editorconfig) para mantener consistencia. Es recomendable instalar su [plugin](https://editorconfig.org/#download) en el IDE que se utilice.

## Scripts

En el directorio `scripts/` hay varios scripts útiles:

- `clone-authors.ps1` - Clona autores entre carpetas
- `optimize-images.ps1` - Optimiza imágenes del proyecto

### Scripts de Python

El subdirectorio `scripts/python/` contiene los scripts de Python:

- **`export_authors_to_excel.py`** - Lee la información en `content/es/authors/` y la escribe, de forma más legible en `authors.xlsx`.
- **`translate_authors_excel.py`** - Añade al archivo `authors.xlsx` las columnas traducidas automáticamente al inglés usando la librería `googletrans`
- **`import_authors_from_excel.py`** - Importa información de `authors.xlsx` y la escribe en los archivos correspondientes en `content/es/authors/` y `content/en/authors/` (aún no implementado) # TODO

Y cuenta con un entorno virtual Python gestionado automáticamente mediante el script:

- **`setup_env.ps1`** - Gestor automático del entorno virtual Python

#### Uso del entorno Python

1. Asegurarse de tener Python 3.8 o superior (`python --version`) instalado.
2. Crear el entorno virtual:

    ```powershell
    python -m venv ./scripts/.venv
    ```

    Al crear el entorno virtual, es posible que el editor o IDE lo detecte y sugiera activarlo.

3. Activar el entorno virtual:

   - En PowerShell:

    ```powershell
    .\scripts\.venv\Scripts\Activate.ps1
    ```

   - En Linux/Mac:

    ```bash
    source ./scripts/.venv/bin/activate
    ```

    Si se ha configurado en el editor o IDE, es posible que este paso no sea necesario.

4. Instalar las dependencias:

    ```powershell
    pip install -r ./scripts/requirements.txt
    ```

Listo! Ya se pueden ejecutar los scripts de Python. Para desactivar el entorno virtual:

```powershell
deactivate
```
