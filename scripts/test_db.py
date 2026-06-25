import os
from urllib.parse import unquote, urlparse, parse_qs

import pymysql
from dotenv import load_dotenv

load_dotenv()


def get_env(name, default=None):
    value = os.getenv(name, default)
    return default if value == "" else value


def config_from_uri(uri: str):
    parsed = urlparse(uri)
    query = parse_qs(parsed.query)
    return {
        "host": parsed.hostname,
        "port": parsed.port or 3306,
        "user": unquote(parsed.username or ""),
        "password": unquote(parsed.password or ""),
        "database": (parsed.path or "/defaultdb").lstrip("/") or "defaultdb",
        "ssl_mode": (query.get("ssl-mode") or query.get("ssl_mode") or ["REQUIRED"])[0],
    }


uri = get_env("MYSQL_URI") or get_env("DATABASE_URL")
if uri:
    cfg = config_from_uri(uri)
else:
    cfg = {
        "host": get_env("MYSQL_HOST"),
        "port": int(get_env("MYSQL_PORT", "3306")),
        "user": get_env("MYSQL_USER"),
        "password": get_env("MYSQL_PASSWORD"),
        "database": get_env("MYSQL_DB", "defaultdb"),
        "ssl_mode": get_env("MYSQL_SSL_MODE", "REQUIRED"),
    }

ssl_mode = str(cfg.pop("ssl_mode", "REQUIRED")).upper()
if ssl_mode not in {"DISABLED", "FALSE", "0", "NO"}:
    cfg["ssl"] = {"check_hostname": False}

connection = pymysql.connect(
    **cfg,
    charset="utf8mb4",
    connect_timeout=10,
    read_timeout=30,
    write_timeout=30,
    cursorclass=pymysql.cursors.DictCursor,
)

with connection:
    with connection.cursor() as cursor:
        cursor.execute("SELECT DATABASE() AS db, VERSION() AS version")
        print(cursor.fetchone())
        cursor.execute("SHOW TABLES")
        print(cursor.fetchall())
