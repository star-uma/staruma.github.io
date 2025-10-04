#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera traducciones automáticas para columnas seleccionadas de authors.xlsx."""

from __future__ import annotations

import argparse
import time
from pathlib import Path
from typing import Dict, Iterable, Tuple
import pandas as pd
from googletrans import Translator

# Columnas a traducir (columna origen, columna destino)
FIELDS_TO_TRANSLATE: Tuple[Tuple[str, str], ...] = (
    ("organizations_text", "organizations_text_en"),
    ("user_groups_text", "user_groups_text_en"),
    ("interests_text", "interests_text_en"),
    ("education_text", "education_text_en"),
    ("bio", "bio_en"),
)


def translate_text(
    text: str,
    translator: Translator,
    cache: Dict[str, str],
    max_retries: int = 3,
    delay: float = 0.1,
) -> str:
    """Traduce un texto del español al inglés reutilizando un caché simple."""
    normalized = text.strip()
    if not normalized:
        return ""

    if normalized in cache:
        return cache[normalized]

    for attempt in range(max_retries):
        try:
            if attempt > 0:
                # Backoff exponencial ligero
                time.sleep(1.5 * attempt)
            else:
                time.sleep(delay)

            result = translator.translate(normalized, src="es", dest="en")
            cache[normalized] = result.text
            return result.text
        except Exception as exc:  # pragma: no cover - manejo runtime API
            print(
                f"⚠️  Error traduciendo '{normalized[:50]}...': {exc}. "
                f"Intento {attempt + 1}/{max_retries}"
            )

    print(f"❌ Se omite traducción tras {max_retries} intentos: '{normalized[:50]}...'")
    cache[normalized] = normalized
    return normalized


def ensure_destination_column(df: pd.DataFrame, source_col: str, dest_col: str) -> None:
    """Inserta la columna destino a la derecha de la columna origen."""
    if source_col not in df.columns:
        raise KeyError(f"La columna origen '{source_col}' no existe en el DataFrame")

    insert_position = int(df.columns.get_indexer([source_col])[0]) + 1

    if dest_col in df.columns:
        df.drop(columns=[dest_col], inplace=True)

    df.insert(insert_position, dest_col, "")


def translate_dataframe(df: pd.DataFrame, translator: Translator) -> Dict[str, int]:
    """Traduce las columnas configuradas y devuelve estadísticas básicas."""
    cache: Dict[str, str] = {}
    stats = {"processed": 0, "translated": 0, "skipped_missing": 0}

    for source_col, dest_col in FIELDS_TO_TRANSLATE:
        if source_col not in df.columns:
            print(f"⚠️  Columna '{source_col}' no encontrada. Se omite su traducción.")
            stats["skipped_missing"] += 1
            continue

        ensure_destination_column(df, source_col, dest_col)
        print(f"📝 Traduciendo '{source_col}' → '{dest_col}'...")

        for idx in df.index:
            value = df.at[idx, source_col]
            stats["processed"] += 1

            if pd.isna(value) or str(value).strip() == "":
                df.at[idx, dest_col] = ""
                continue

            text = str(value)
            translation = translate_text(text, translator, cache)
            df.at[idx, dest_col] = translation

            if translation != text:
                stats["translated"] += 1

    return stats


def auto_adjust_column_widths(writer: pd.ExcelWriter, sheet_name: str) -> None:
    """Ajusta el ancho de columnas para mejorar la legibilidad en Excel."""
    worksheet = writer.sheets[sheet_name]
    for column_cells in worksheet.columns:
        max_length = 0
        column_letter = column_cells[0].column_letter

        for cell in column_cells:
            try:
                cell_value = "" if cell.value is None else str(cell.value)
                max_length = max(max_length, len(cell_value))
            except Exception:
                continue

        worksheet.column_dimensions[column_letter].width = min(max_length + 2, 60)


def translate_excel(input_path: Path, output_path: Path, sheet_name: str = "Autores") -> Dict[str, int]:
    """Lee el Excel, traduce columnas y guarda el resultado."""
    if not input_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {input_path}")

    print(f"📖 Leyendo datos desde: {input_path}")
    df = pd.read_excel(input_path, sheet_name=sheet_name)
    print(f"📋 Columnas detectadas: {df.columns.tolist()}")

    translator = Translator()
    stats = translate_dataframe(df, translator)

    print(f"💾 Guardando resultados en: {output_path}")
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)
        auto_adjust_column_widths(writer, sheet_name)

    return stats


def parse_args(args: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Traduce columnas seleccionadas de authors.xlsx al inglés."
    )
    parser.add_argument(
        "--input",
        default=Path("authors.xlsx"),
        type=Path,
        help="Ruta al archivo Excel de entrada (por defecto authors.xlsx en el proyecto)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Ruta de salida opcional. Si no se indica, se sobrescribe el archivo de entrada.",
    )
    parser.add_argument(
        "--sheet",
        default="Autores",
        help="Nombre de la hoja a procesar (por defecto 'Autores').",
    )
    sequence_args = list(args) if args is not None else None
    return parser.parse_args(sequence_args)


def main() -> None:
    args = parse_args()
    input_path = args.input.resolve()
    output_path = args.output.resolve() if args.output else input_path

    print("🚀 Iniciando traducción automática de autores...")
    print(f"📂 Archivo de entrada: {input_path}")
    print(f"🗂️  Archivo de salida: {output_path}")
    print(f"📄 Hoja seleccionada: {args.sheet}")

    stats = translate_excel(input_path, output_path, sheet_name=args.sheet)

    print("✅ Traducción completada")
    print(f"   ↳ Registros procesados: {stats['processed']}")
    print(f"   ↳ Traducciones aplicadas: {stats['translated']}")
    print(f"   ↳ Columnas omitidas por falta de origen: {stats['skipped_missing']}")
if __name__ == "__main__":
    main()
