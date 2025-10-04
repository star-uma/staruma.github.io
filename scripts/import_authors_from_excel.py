#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Importa autores desde ``authors.xlsx`` a los contenidos de Hugo."""

from __future__ import annotations

import argparse
import re
from collections import OrderedDict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional

import pandas as pd
import yaml

PROJECT_REL_ES = Path("content/es/authors")
PROJECT_REL_EN = Path("content/en/authors")
DEFAULT_INPUT = Path("authors.xlsx")
DEFAULT_SHEET = "Autores"

SOCIAL_ICON_PACK = {
    "email": ("envelope", "fas"),
    "github": ("github", "fab"),
    "x-twitter": ("x-twitter", "fab"),
    "linkedin": ("linkedin", "fab"),
    "instagram": ("instagram", "fab"),
}

LIST_SEPARATORS = re.compile(r"[,;\n]")
ORG_SEPARATORS = re.compile(r"[;\n]")


@dataclass
class AuthorContent:
    """Resultado del procesado de una fila del Excel."""

    slug: str
    frontmatter: OrderedDict
    body: str | None
    language: str

    def target_path(self, root: Path) -> Path:
        base_dir = PROJECT_REL_ES if self.language == "es" else PROJECT_REL_EN
        return root / base_dir / self.slug / "_index.md"


def coerce_bool(value) -> Optional[bool]:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    if isinstance(value, bool):
        return value
    try:
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            return bool(int(value))
    except (TypeError, ValueError):
        pass
    text = str(value).strip().lower()
    if not text:
        return None
    return text in {"true", "1", "yes", "y", "si", "sí"}


def clean_text(value) -> str:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ""
    if isinstance(value, str):
        return value.strip().replace("\\/", "/")
    return str(value).strip()


def get_lang_text(row: pd.Series, base: str, language: str) -> str:
    suffix = "_en" if language == "en" else ""
    column = f"{base}{suffix}" if suffix else base
    text = clean_text(row.get(column))
    if text:
        return text
    # fallback al español si falta la traducción
    if suffix:
        return clean_text(row.get(base))
    return text


def parse_simple_list(text: str) -> List[str]:
    if not text:
        return []
    return [item.strip() for item in LIST_SEPARATORS.split(text) if item.strip()]


def parse_organizations(text: str) -> List[OrderedDict]:
    if not text:
        return []
    organizations: List[OrderedDict] = []
    for raw in ORG_SEPARATORS.split(text):
        item = raw.strip()
        if not item:
            continue
        name = item
        url = ""
        if "(" in item and item.endswith(")"):
            name_part, url_part = item.rsplit("(", 1)
            name = name_part.strip()
            url = url_part.strip().rstrip(")").strip()
        if name:
            org = OrderedDict()
            org["name"] = name
            if url:
                org["url"] = url
            organizations.append(org)
    return organizations


def parse_education(text: str) -> Optional[OrderedDict]:
    if not text:
        return None
    entries: List[OrderedDict] = []
    for raw in ORG_SEPARATORS.split(text):
        item = raw.strip()
        if not item:
            continue
        year = ""
        year_match = re.search(r"\(([^()]*)\)\s*$", item)
        if year_match:
            year = year_match.group(1).strip()
            item = item[:year_match.start()].strip()
        course = item
        institution = ""
        if " - " in item:
            course_part, institution_part = item.split(" - ", 1)
            course = course_part.strip()
            institution = institution_part.strip()
        entry = OrderedDict()
        entry["course"] = course
        if institution:
            entry["institution"] = institution
        if year:
            entry["year"] = year
        entries.append(entry)
    if not entries:
        return None
    return OrderedDict({"courses": entries})


def build_social(row: pd.Series) -> List[OrderedDict]:
    social_entries: List[OrderedDict] = []
    processed: set[str] = set()
    for suffix, (icon, icon_pack) in SOCIAL_ICON_PACK.items():
        column = f"social_{suffix}"
        value = clean_text(row.get(column))
        if not value:
            continue
        processed.add(column)
        if suffix == "email" and not value.startswith("mailto:"):
            value = f"mailto:{value}"
        social_entries.append(
            OrderedDict({"icon": icon, "icon_pack": icon_pack, "link": value})
        )

    # Capturar columnas sociales adicionales
    for column in row.index:
        if not column.startswith("social_") or column in processed:
            continue
        link = clean_text(row.get(column))
        if not link:
            continue
        suffix = column.split("social_", 1)[1]
        icon = suffix
        icon_pack = "fas" if suffix == "envelope" else "fab"
        social_entries.append(
            OrderedDict({"icon": icon, "icon_pack": icon_pack, "link": link})
        )
    return social_entries


def build_author_content(slug: str, row: pd.Series, language: str) -> AuthorContent:
    fm = OrderedDict()
    if language == "en":
        fm["translationKey"] = slug

    title = clean_text(row.get("title"))
    if title:
        fm["title"] = title

    first_name = clean_text(row.get("first_name"))
    if first_name:
        fm["first_name"] = first_name

    last_name = clean_text(row.get("last_name"))
    if last_name:
        fm["last_name"] = last_name

    superuser = coerce_bool(row.get("superuser"))
    if superuser is not None:
        fm["superuser"] = superuser

    role = clean_text(row.get("role"))
    if role:
        fm["role"] = role if language == "es" else get_lang_text(row, "role", language)

    organizations = parse_organizations(get_lang_text(row, "organizations_text", language))
    if organizations:
        fm["organizations"] = organizations

    bio = get_lang_text(row, "bio", language)
    if bio:
        fm["bio"] = bio

    interests = parse_simple_list(get_lang_text(row, "interests_text", language))
    if interests:
        fm["interests"] = interests

    education = parse_education(get_lang_text(row, "education_text", language))
    if education:
        fm["education"] = education

    social_links = build_social(row)
    if social_links:
        fm["social"] = social_links

    email = clean_text(row.get("email"))
    if email:
        fm["email"] = email

    highlight_name = coerce_bool(row.get("highlight_name"))
    if highlight_name is not None:
        fm["highlight_name"] = highlight_name

    user_groups = parse_simple_list(get_lang_text(row, "user_groups_text", language))
    if user_groups:
        fm["user_groups"] = user_groups

    body_column = "body_en" if language == "en" else "body"
    body_text = clean_text(row.get(body_column))
    body = body_text if body_text else None

    return AuthorContent(slug=slug, frontmatter=fm, body=body, language=language)


def render_markdown(frontmatter: OrderedDict, body: str | None) -> str:
    yaml_content = yaml.safe_dump(
        _to_builtin(frontmatter), sort_keys=False, allow_unicode=True
    ).strip()
    markdown_parts = ["---", yaml_content, "---"]
    if body:
        markdown_parts.append("")
        markdown_parts.append(body)
    markdown_parts.append("")
    return "\n".join(markdown_parts)


def _to_builtin(value):
    """Convierte estructuras basadas en OrderedDict a tipos estándar."""

    if isinstance(value, OrderedDict):
        return {key: _to_builtin(val) for key, val in value.items()}
    if isinstance(value, list):
        return [_to_builtin(item) for item in value]
    if isinstance(value, tuple):
        return tuple(_to_builtin(item) for item in value)
    return value


def ensure_directory(path: Path, dry_run: bool) -> None:
    if dry_run:
        return
    path.mkdir(parents=True, exist_ok=True)


def write_author(content: AuthorContent, root: Path, dry_run: bool, verbose: bool) -> None:
    target = content.target_path(root)
    ensure_directory(target.parent, dry_run)
    if dry_run:
        if verbose:
            print(f"[dry-run] {content.language} → {target}")
        return
    target.write_text(render_markdown(content.frontmatter, content.body), encoding="utf-8")
    if verbose:
        print(f"✓ Escrito: {target.relative_to(root)}")


def parse_args(args: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Genera los archivos `_index.md` de autores a partir de authors.xlsx")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="Ruta al archivo authors.xlsx")
    parser.add_argument("--sheet", default=DEFAULT_SHEET, help="Nombre de la hoja dentro del Excel")
    parser.add_argument("--dry-run", action="store_true", help="Muestra qué archivos se generarían sin escribir nada")
    parser.add_argument("--only", nargs="*", help="Lista opcional de slugs a procesar")
    parser.add_argument("--verbose", action="store_true", help="Imprime información adicional durante el proceso")
    sequence_args = list(args) if args is not None else None
    return parser.parse_args(sequence_args)


def resolve_path(root: Path, path: Path) -> Path:
    return path if path.is_absolute() else root / path


def main(cli_args: Iterable[str] | None = None) -> None:
    args = parse_args(cli_args)
    script_path = Path(__file__).resolve()
    project_root = script_path.parent.parent

    input_path = resolve_path(project_root, args.input)
    if not input_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo Excel: {input_path}")

    df = pd.read_excel(input_path, sheet_name=args.sheet)
    if df.empty:
        print("⚠️  No hay filas en el Excel. Nada que procesar.")
        return

    slugs_filter = {slug.strip() for slug in args.only} if args.only else None

    processed = written = 0

    for _, row in df.iterrows():
        slug = clean_text(row.get("folder_name"))
        if not slug:
            continue
        if slugs_filter and slug not in slugs_filter:
            continue

        processed += 1

        es_content = build_author_content(slug, row, "es")
        en_content = build_author_content(slug, row, "en")

        write_author(es_content, project_root, args.dry_run, args.verbose)
        write_author(en_content, project_root, args.dry_run, args.verbose)
        written += 1

    summary = f"Procesados: {processed} autores"
    if args.dry_run:
        summary += " (simulación)"
    print(summary)
    if processed and not args.dry_run:
        print(f"Archivos escritos: {written * 2}")


if __name__ == "__main__":
    main()
