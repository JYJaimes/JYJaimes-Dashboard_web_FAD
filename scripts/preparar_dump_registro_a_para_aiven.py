"""Prepara el dump grande c19pruebas_registro_a.sql para importarlo en Aiven/defaultdb.

Uso en Windows desde la carpeta del proyecto:

python scripts/preparar_dump_registro_a_para_aiven.py "D:\\ruta\\c19pruebas_registro_a.sql" "D:\\ruta\\registro_a_defaultdb.sql"

Qué hace:
- Agrega USE `defaultdb`; al inicio.
- Quita LOCK TABLES y UNLOCK TABLES.
- Quita ALTER TABLE ... DISABLE/ENABLE KEYS.
- Quita CREATE DATABASE y USE de otras bases si existieran.
- Mantiene los INSERT INTO `registro_a`.
"""
from __future__ import annotations

import sys
from pathlib import Path

SKIP_PREFIXES = (
    "LOCK TABLES",
    "UNLOCK TABLES",
    "CREATE DATABASE",
    "USE ",
)

SKIP_CONTAINS = (
    "DISABLE KEYS",
    "ENABLE KEYS",
)


def should_skip(line: str) -> bool:
    stripped = line.strip()
    upper = stripped.upper()
    if not stripped:
        return False
    if any(upper.startswith(prefix) for prefix in SKIP_PREFIXES):
        return True
    if any(token in upper for token in SKIP_CONTAINS):
        return True
    return False


def prepare(input_path: Path, output_path: Path, database: str = "defaultdb") -> None:
    with input_path.open("r", encoding="utf-8", errors="ignore") as src, output_path.open("w", encoding="utf-8", newline="\n") as dst:
        dst.write(f"USE `{database}`;\n")
        dst.write("SET FOREIGN_KEY_CHECKS=0;\n")
        dst.write("SET UNIQUE_CHECKS=0;\n\n")
        for line in src:
            if should_skip(line):
                continue
            dst.write(line)
        dst.write("\nSET UNIQUE_CHECKS=1;\n")
        dst.write("SET FOREIGN_KEY_CHECKS=1;\n")


if __name__ == "__main__":
    if len(sys.argv) not in {3, 4}:
        print("Uso: python scripts/preparar_dump_registro_a_para_aiven.py entrada.sql salida.sql [base]")
        sys.exit(1)

    entrada = Path(sys.argv[1])
    salida = Path(sys.argv[2])
    base = sys.argv[3] if len(sys.argv) == 4 else "defaultdb"

    if not entrada.exists():
        print(f"No existe el archivo de entrada: {entrada}")
        sys.exit(1)

    prepare(entrada, salida, base)
    print(f"Dump preparado para Aiven/defaultdb: {salida}")
