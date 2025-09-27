# Scripts de Python - RoboRescue UMA

Este directorio contiene scripts de Python para procesar y exportar datos del proyecto RoboRescue UMA.

## Entorno Virtual

Para evitar conflictos de librerías, todos los scripts deben ejecutarse dentro de un entorno virtual aislado.

### Configuración Inicial

1. **Configurar el entorno automáticamente:**
   ```powershell
   .\setup_env.ps1 setup
   ```

2. **O configurarlo manualmente:**
   ```powershell
   # Crear entorno virtual
   python -m venv venv

   # Activar entorno virtual
   .\venv\Scripts\Activate.ps1

   # Instalar dependencias
   pip install -r requirements.txt
   ```

### Uso Diario

#### Opción 1: Script automatizado (Recomendado)
```powershell
# Ejecutar directamente el script de exportación
.\setup_env.ps1 run

# Ver ayuda de comandos disponibles
.\setup_env.ps1 help
```

#### Opción 2: Activación manual
```powershell
# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Ejecutar script
python export_authors_to_excel.py

# Desactivar cuando termines
deactivate
```

### Comandos del Gestor de Entorno

El script `setup_env.ps1` proporciona los siguientes comandos:

- **`setup`** - Crear entorno virtual e instalar dependencias
- **`run`** - Ejecutar el script de exportación
- **`activate`** - Mostrar cómo activar el entorno virtual
- **`install`** - Instalar/actualizar dependencias
- **`clean`** - Eliminar el entorno virtual completamente
- **`help`** - Mostrar ayuda detallada

### Scripts Disponibles

#### `export_authors_to_excel.py`
Exporta información de todos los autores del directorio `content/es/authors/` a un archivo Excel.

**Funcionalidades:**
- Lee archivos `_index.md` y extrae metadatos YAML
- Detecta archivos de avatar automáticamente
- Procesa enlaces sociales, organizaciones, educación e intereses
- **🌐 Traduce automáticamente** campos al inglés usando Google Translate
- Genera un archivo `authors.xlsx` en la raíz del proyecto
- Ajusta automáticamente el ancho de las columnas en Excel

**Campos traducidos automáticamente:**
- `role` → `role_en`
- `organizations_text` → `organizations_text_en`
- `user_groups_text` → `user_groups_text_en`
- `interests_text` → `interests_text_en`
- `education_text` → `education_text_en`
- `bio` → `bio_en`

**Salida:**
- Archivo: `../../authors.xlsx` (raíz del proyecto)
- Formato: Excel con hoja "Autores"
- Datos: 43 autores procesados, 26 con avatar, 29 columnas de información
- Traducciones: ~180 campos traducidos automáticamente del español al inglés

### Estructura del Entorno

```
python/
├── venv/                   # Entorno virtual (creado automáticamente)
├── export_authors_to_excel.py  # Script principal
├── requirements.txt        # Dependencias
├── setup_env.ps1          # Gestor del entorno
└── README.md              # Esta documentación
```

### Dependencias

- **pandas** (≥1.5.0) - Manipulación de datos y exportación a Excel
- **openpyxl** (≥3.0.0) - Creación y edición de archivos Excel
- **PyYAML** (≥6.0) - Procesamiento de metadatos YAML
- **googletrans** (4.0.0-rc1) - Traducción automática español-inglés

### Resolución de Problemas

1. **Error de permisos en PowerShell:**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

2. **El entorno virtual no se activa:**
   - Asegúrate de estar en el directorio `scripts/python/`
   - Verifica que existe la carpeta `venv/`

3. **Error al instalar dependencias:**
   - Verifica tu conexión a internet
   - Actualiza pip: `python -m pip install --upgrade pip`

4. **El script no encuentra los archivos:**
   - Verifica que estás ejecutando desde `scripts/python/`
   - Asegúrate de que existe `content/es/authors/`

### Mantenimiento

- **Actualizar dependencias:** `.\setup_env.ps1 install`
- **Limpiar entorno:** `.\setup_env.ps1 clean`
- **Recrear entorno:** `.\setup_env.ps1 clean` seguido de `.\setup_env.ps1 setup`

---

**Nota:** Siempre usa el entorno virtual para ejecutar los scripts de Python. Esto garantiza que las dependencias estén aisladas y no interfieran con otros proyectos.
