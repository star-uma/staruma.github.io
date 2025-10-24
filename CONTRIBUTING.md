# Contribuir

- Documentación de HugoBlox: <https://docs.hugoblox.com/>
- El repositorio cuenta con un archivo [.editorconfig](.editorconfig) para mantener consistencia. Es recomendable instalar su [plugin](https://editorconfig.org/#download) en el IDE que se utilice.

## Scripts

En el directorio `scripts/` hay varios scripts útiles, tanto en PowerShell como en Python. Los scripts de PowerShell no requieren configuración adicional, mientras que para los de Python, es recomendable crear un entorno virtual (ver más abajo).

- `clone-authors.ps1` - Clona autores entre carpetas
- `optimize-images.ps1` - Optimiza imágenes del proyecto

### Scripts de Python

Además de los anteriores, el directorio `scripts/` contiene varios scripts de Python:

- **`export_authors_to_excel.py`** - Lee la información en `content/es/authors/` y la escribe, de forma más legible en un archivo `authors.xlsx`.
- **`translate_authors_excel.py`** - Añade al archivo `authors.xlsx` las columnas traducidas automáticamente al inglés usando la librería `googletrans`
- **`import_authors_from_excel.py`** - Importa información de `authors.xlsx` y la escribe en los archivos correspondientes en `content/es/authors/` y `content/en/authors/` (aún no implementado) # TODO

Y cuenta con un entorno virtual Python gestionado automáticamente mediante el script:

- **`scripts/.venv/Scripts/setup_env.ps1`** - Gestor automático del entorno virtual Python

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
