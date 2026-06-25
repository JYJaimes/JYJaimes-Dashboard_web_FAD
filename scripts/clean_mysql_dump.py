"""Limpia dumps MySQL para importarlos más fácil en servicios administrados.

Uso:
    python scripts/clean_mysql_dump.py entrada.sql salida.sql

Elimina líneas que suelen fallar por permisos limitados:
- LOCK TABLES
- UNLOCK TABLES
- ALTER TABLE ... DISABLE/ENABLE KEYS
- comentarios condicionales relacionados con FOREIGN_KEY_CHECKS/UNIQUE_CHECKS si estorban
"""
from __future__ import annotations

import sys
from pathlib import Path

SKIP_PREFIXES = (
    "LOCK TABLES",
    "UNLOCK TABLES",
)
SKIP_CONTAINS = (
    "DISABLE KEYS",
    "ENABLE KEYS",
)


def clean(input_path: Path, output_path: Path) -> None:
    with input_path.open("r", encoding="utf-8", errors="ignore") as src, output_path.open("w", encoding="utf-8") as dst:
        for line in src:
            stripped = line.strip()
            if any(stripped.startswith(prefix) for prefix in SKIP_PREFIXES):
                continue
            if any(token in stripped for token in SKIP_CONTAINS):
                continue
            dst.write(line)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python scripts/clean_mysql_dump.py entrada.sql salida.sql")
        sys.exit(1)
    clean(Path(sys.argv[1]), Path(sys.argv[2]))
    print(f"Dump limpio creado en: {sys.argv[2]}")
