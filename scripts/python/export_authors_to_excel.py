#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para exportar información de autores a Excel
Lee todas las carpetas y archivos en content/es/authors y los exporta a authors.xlsx
Con traducción automática de campos al inglés usando Google Translate
"""

import os
import pandas as pd
from pathlib import Path
import yaml
from typing import Dict, List, Any
import re
import time
from googletrans import Translator

def read_markdown_frontmatter(file_path: str) -> Dict[str, Any]:
    """
    Lee el frontmatter YAML de un archivo markdown.

    Args:
        file_path: Ruta al archivo markdown

    Returns:
        Diccionario con los datos del frontmatter
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Buscar el frontmatter YAML entre ---
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 2:
                frontmatter = parts[1].strip()
                try:
                    return yaml.safe_load(frontmatter) or {}
                except yaml.YAMLError as e:
                    print(f"Error parseando YAML en {file_path}: {e}")
                    return {}
        return {}
    except Exception as e:
        print(f"Error leyendo {file_path}: {e}")
        return {}

def extract_social_links(social_data: List[Dict]) -> Dict[str, str]:
    """
    Extrae los enlaces sociales y los convierte en columnas separadas.

    Args:
        social_data: Lista de diccionarios con información social

    Returns:
        Diccionario con enlaces sociales
    """
    social_links = {}

    if not isinstance(social_data, list):
        return social_links

    for social in social_data:
        if isinstance(social, dict) and 'icon' in social and 'link' in social:
            icon = social['icon']
            link = social['link']

            # Mapear iconos específicos para consistencia
            if icon == 'envelope':
                social_links['social_email'] = link
            elif icon == 'x-twitter':
                social_links['social_x-twitter'] = link
            else:
                social_links[f'social_{icon}'] = link

    return social_links

def flatten_organizations(orgs_data: List[Dict]) -> str:
    """
    Convierte la lista de organizaciones en una cadena de texto.

    Args:
        orgs_data: Lista de diccionarios con información de organizaciones

    Returns:
        Cadena con las organizaciones separadas por ;
    """
    if not isinstance(orgs_data, list):
        return ""

    org_strings = []
    for org in orgs_data:
        if isinstance(org, dict):
            name = org.get('name', '')
            url = org.get('url', '')
            if name:
                if url:
                    org_strings.append(f"{name} ({url})")
                else:
                    org_strings.append(name)

    return "; ".join(org_strings)

def flatten_list_field(data: List) -> str:
    """
    Convierte una lista en una cadena de texto separada por comas.

    Args:
        data: Lista de elementos

    Returns:
        Cadena con elementos separados por comas
    """
    if not isinstance(data, list):
        return str(data) if data else ""

    return ", ".join([str(item) for item in data if item])

def translate_text(text: str, translator: Translator, max_retries: int = 3) -> str:
    """
    Traduce un texto del español al inglés usando Google Translate.

    Args:
        text: Texto a traducir
        translator: Instancia del traductor
        max_retries: Número máximo de reintentos

    Returns:
        Texto traducido o texto original si falla
    """
    if not text or text.strip() == "":
        return ""

    for attempt in range(max_retries):
        try:
            # Pausa breve para evitar rate limiting
            time.sleep(0.1)

            # Traducir del español al inglés
            result = translator.translate(text, src='es', dest='en')
            return result.text

        except Exception as e:
            print(f"⚠️  Error traduciendo '{text[:50]}...': {e}")
            if attempt < max_retries - 1:
                print(f"🔄 Reintentando... ({attempt + 1}/{max_retries})")
                time.sleep(1)  # Pausa más larga antes de reintentar
            else:
                print(f"❌ Falló traducción después de {max_retries} intentos")
                return text  # Devolver texto original

    return text

def translate_dataframe_columns(df: pd.DataFrame, translator: Translator) -> pd.DataFrame:
    """
    Traduce las columnas que terminan en '_en' usando Google Translate.

    Args:
        df: DataFrame con los datos
        translator: Instancia del traductor

    Returns:
        DataFrame con traducciones completadas
    """
    print("🌐 Iniciando traducción automática al inglés...")

    # Campos que deben ser traducidos
    fields_to_translate = [
        ('role', 'role_en'),
        ('organizations_text', 'organizations_text_en'),
        ('user_groups_text', 'user_groups_text_en'),
        ('interests_text', 'interests_text_en'),
        ('education_text', 'education_text_en'),
        ('bio', 'bio_en')
    ]

    total_translations = 0
    successful_translations = 0

    for spanish_col, english_col in fields_to_translate:
        if spanish_col in df.columns and english_col in df.columns:
            print(f"📝 Traduciendo {spanish_col} -> {english_col}...")

            for idx in df.index:
                spanish_text = df.loc[idx, spanish_col]

                if pd.notna(spanish_text) and str(spanish_text).strip() != "":
                    total_translations += 1
                    english_text = translate_text(str(spanish_text), translator)
                    df.loc[idx, english_col] = english_text

                    if english_text != str(spanish_text):  # Se tradujo exitosamente
                        successful_translations += 1

                    # Mostrar progreso cada 10 traducciones
                    if total_translations % 10 == 0:
                        print(f"   📊 Progreso: {total_translations} textos procesados...")

    print(f"✅ Traducción completada:")
    print(f"   📈 Total procesados: {total_translations}")
    print(f"   ✨ Traducidos exitosamente: {successful_translations}")
    print(f"   📋 Sin cambios (ya en inglés/errores): {total_translations - successful_translations}")

    return df

def scan_authors_directory(authors_path: str) -> List[Dict[str, Any]]:
    """
    Escanea el directorio de autores y extrae información.

    Args:
        authors_path: Ruta al directorio de autores

    Returns:
        Lista de diccionarios con información de cada autor
    """
    authors_data = []
    authors_dir = Path(authors_path)

    if not authors_dir.exists():
        print(f"El directorio {authors_path} no existe.")
        return authors_data

    print(f"Escaneando directorio: {authors_path}")

    # Iterar por cada carpeta de autor
    for author_folder in sorted(authors_dir.iterdir()):
        if author_folder.is_dir():
            print(f"Procesando: {author_folder.name}")

            author_info = {
                'folder_name': author_folder.name,
                'has_index': False,
                'has_avatar': False,
                'avatar_files': [],
                'other_files': [],
                'total_files': 0
            }

            # Buscar archivos en la carpeta del autor
            files_found = list(author_folder.iterdir())
            author_info['total_files'] = len([f for f in files_found if f.is_file()])

            for file_path in files_found:
                if file_path.is_file():
                    file_name = file_path.name.lower()

                    if file_name == '_index.md':
                        author_info['has_index'] = True
                        # Leer información del frontmatter
                        frontmatter = read_markdown_frontmatter(str(file_path))

                        # Procesar campos especiales
                        if 'social' in frontmatter:
                            social_links = extract_social_links(frontmatter['social'])
                            author_info.update(social_links)
                            # Remover el campo social original para evitar problemas
                            del frontmatter['social']

                        if 'organizations' in frontmatter:
                            author_info['organizations_text'] = flatten_organizations(frontmatter['organizations'])
                            del frontmatter['organizations']

                        if 'user_groups' in frontmatter:
                            author_info['user_groups_text'] = flatten_list_field(frontmatter['user_groups'])
                            del frontmatter['user_groups']

                        if 'interests' in frontmatter:
                            author_info['interests_text'] = flatten_list_field(frontmatter['interests'])
                            del frontmatter['interests']

                        if 'education' in frontmatter and isinstance(frontmatter['education'], dict):
                            if 'courses' in frontmatter['education']:
                                courses = frontmatter['education']['courses']
                                if isinstance(courses, list):
                                    course_strings = []
                                    for course in courses:
                                        if isinstance(course, dict):
                                            course_str = course.get('course', '')
                                            institution = course.get('institution', '')
                                            year = course.get('year', '')
                                            if course_str:
                                                course_info = course_str
                                                if institution:
                                                    course_info += f" - {institution}"
                                                if year:
                                                    course_info += f" ({year})"
                                                course_strings.append(course_info)
                                    author_info['education_text'] = "; ".join(course_strings)
                            del frontmatter['education']

                        # Agregar el resto de campos del frontmatter
                        for key, value in frontmatter.items():
                            if key == 'email' and value:
                                # Convertir email a formato social_email para consistencia
                                if not value.startswith('mailto:'):
                                    author_info['social_email'] = f'mailto:{value}'
                                else:
                                    author_info['social_email'] = value
                            elif key in ['highlight_name']:
                                # Mantener campos específicos como están
                                author_info[key] = value
                            else:
                                author_info[key] = value

                    elif 'avatar' in file_name:
                        author_info['has_avatar'] = True
                        author_info['avatar_files'].append(file_path.name)

                    else:
                        author_info['other_files'].append(file_path.name)

            # Convertir listas a strings para Excel
            author_info['avatar_files'] = ', '.join(author_info['avatar_files'])
            author_info['other_files'] = ', '.join(author_info['other_files'])

            authors_data.append(author_info)

    return authors_data

def export_to_excel(authors_data: List[Dict[str, Any]], output_path: str, use_translation: bool = True):
    """
    Exporta los datos de autores a un archivo Excel.

    Args:
        authors_data: Lista con datos de autores
        output_path: Ruta del archivo Excel de salida
        use_translation: Si True, traduce automáticamente los campos al inglés
    """
    try:
        if not authors_data:
            print("No hay datos para exportar.")
            return

        df = pd.DataFrame(authors_data)

        # Agregar columnas vacías para las versiones en inglés
        for col in ['role', 'organizations_text', 'user_groups_text', 'interests_text', 'education_text', 'bio']:
            if col in df.columns:
                df[f'{col}_en'] = ""

        # Traducir campos al inglés si está habilitado
        if use_translation:
            try:
                translator = Translator()
                df = translate_dataframe_columns(df, translator)
            except Exception as e:
                print(f"⚠️  Error en traducción automática: {e}")
                print("📋 Continuando sin traducir (columnas en inglés quedarán vacías)...")

        # Reordenar columnas según el formato actual del Excel
        priority_columns = [
            'folder_name', 'title', 'first_name', 'last_name', 'superuser',
            'role', 'role_en',
            'organizations_text', 'organizations_text_en',
            'user_groups_text', 'user_groups_text_en',
            'interests_text', 'interests_text_en',
            'education_text', 'education_text_en',
            'bio', 'bio_en'
        ]

        # Agregar columnas de información adicional del archivo
        info_columns = [
            'has_index', 'has_avatar', 'total_files', 'avatar_files', 'other_files'
        ]

        # Obtener columnas sociales en orden específico (igual al formato actual)
        social_order = ['email', 'github', 'x-twitter', 'linkedin', 'instagram']
        social_columns = []
        for social in social_order:
            col_name = f'social_{social}'
            if col_name in df.columns:
                social_columns.append(col_name)

        # Agregar cualquier columna social adicional no listada
        other_social = [col for col in df.columns if col.startswith('social_') and col not in social_columns]
        social_columns.extend(sorted(other_social))

        # Obtener otras columnas no categorizadas
        all_categorized = priority_columns + info_columns + social_columns
        other_columns = [col for col in df.columns if col not in all_categorized]
        other_columns.sort()

        # Crear orden final de columnas disponibles
        available_priority = [col for col in priority_columns if col in df.columns]
        available_info = [col for col in info_columns if col in df.columns]
        final_columns = available_priority + social_columns + available_info + other_columns

        df = df.reindex(columns=final_columns)

        # Guardar en Excel
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Autores', index=False)

            # Ajustar ancho de columnas
            worksheet = writer.sheets['Autores']
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter

                for cell in column:
                    try:
                        cell_value = str(cell.value) if cell.value is not None else ""
                        if len(cell_value) > max_length:
                            max_length = len(cell_value)
                    except:
                        pass

                # Limitar el ancho máximo para evitar columnas demasiado anchas
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width

        print(f"✅ Archivo Excel creado exitosamente: {output_path}")
        print(f"📊 Total de autores procesados: {len(authors_data)}")
        print(f"📋 Columnas exportadas: {len(df.columns)}")

        # Mostrar estadísticas básicas
        if 'has_avatar' in df.columns:
            has_avatar = df['has_avatar'].sum()
            print(f"👤 Autores con avatar: {has_avatar}")

        if 'has_index' in df.columns:
            has_index = df['has_index'].sum()
            print(f"� Autores con _index.md: {has_index}")

        if 'role' in df.columns:
            roles_count = df['role'].notna().sum()
            print(f"💼 Autores con rol definido: {roles_count}")

        if 'bio' in df.columns:
            bio_count = df['bio'].notna().sum()
            print(f"� Autores con biografía: {bio_count}")

        # Mostrar columnas sociales encontradas
        social_cols = [col for col in df.columns if col.startswith('social_')]
        if social_cols:
            print(f"🔗 Redes sociales detectadas: {len(social_cols)} tipos")

        # Mostrar información sobre traducciones
        en_cols = [col for col in df.columns if col.endswith('_en')]
        if use_translation:
            filled_en_cols = sum(1 for col in en_cols if df[col].notna().sum() > 0)
            print(f"🌐 Columnas traducidas automáticamente: {filled_en_cols}/{len(en_cols)}")
        else:
            print(f"🌐 Columnas en inglés creadas (vacías para fórmulas TRANSLATE): {len(en_cols)}")

    except Exception as e:
        print(f"❌ Error al crear el archivo Excel: {e}")
        raise

def main():
    """Función principal del script."""
    print("🚀 Iniciando exportación de autores a Excel...")
    print("🌐 Con traducción automática al inglés habilitada")

    # Rutas
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent  # Subir dos niveles desde scripts/python
    authors_path = project_root / "content" / "es" / "authors"
    output_path = project_root / "authors.xlsx"

    print(f"📂 Directorio de autores: {authors_path}")
    print(f"📊 Archivo de salida: {output_path}")

    # Verificar que existe el directorio
    if not authors_path.exists():
        print(f"❌ Error: El directorio {authors_path} no existe.")
        return

    # Escanear autores
    authors_data = scan_authors_directory(str(authors_path))

    if authors_data:
        # Exportar a Excel con traducción automática
        export_to_excel(authors_data, str(output_path), use_translation=True)
        print("✅ Proceso completado exitosamente!")
    else:
        print("❌ No se encontraron datos de autores para exportar.")

if __name__ == "__main__":
    main()
