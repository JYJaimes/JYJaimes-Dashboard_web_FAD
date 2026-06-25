import os
from functools import lru_cache
from urllib.parse import unquote, urlparse, parse_qs

import numpy as np
import pandas as pd
from flask import Flask, render_template, request
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.exc import SQLAlchemyError
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


def get_env(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name, default)
    if value == "":
        return default
    return value


def parse_mysql_uri(uri: str) -> dict:
    """Permite usar la URI completa de Aiven si prefieres MYSQL_URI.

    Ejemplo de Aiven:
    mysql://usuario:password@host:puerto/defaultdb?ssl-mode=REQUIRED
    """
    parsed = urlparse(uri)
    query = parse_qs(parsed.query)
    return {
        "host": parsed.hostname,
        "port": parsed.port or 3306,
        "user": unquote(parsed.username or ""),
        "password": unquote(parsed.password or ""),
        "db": (parsed.path or "/defaultdb").lstrip("/") or "defaultdb",
        "ssl_mode": (query.get("ssl-mode") or query.get("ssl_mode") or ["REQUIRED"])[0],
    }


@lru_cache(maxsize=1)
def get_engine():
    """Crea una conexión a MySQL/Aiven usando variables de entorno.

    Opción recomendada en Render:
    MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, MYSQL_SSL_MODE

    También acepta MYSQL_URI si pegas la URI completa de Aiven.
    """
    uri = get_env("MYSQL_URI") or get_env("DATABASE_URL")
    if uri:
        cfg = parse_mysql_uri(uri)
        host = cfg["host"]
        port = int(cfg["port"] or 3306)
        user = cfg["user"]
        password = cfg["password"]
        db = cfg["db"]
        ssl_mode = str(get_env("MYSQL_SSL_MODE", cfg.get("ssl_mode", "REQUIRED"))).upper()
    else:
        host = get_env("MYSQL_HOST")
        port = int(get_env("MYSQL_PORT", "3306"))
        user = get_env("MYSQL_USER")
        password = get_env("MYSQL_PASSWORD")
        db = get_env("MYSQL_DB", "defaultdb")
        ssl_mode = str(get_env("MYSQL_SSL_MODE", "REQUIRED")).upper()

    missing = [k for k, v in {
        "MYSQL_HOST/MYSQL_URI": host,
        "MYSQL_USER/MYSQL_URI": user,
        "MYSQL_PASSWORD/MYSQL_URI": password,
        "MYSQL_DB/MYSQL_URI": db,
    }.items() if not v]
    if missing:
        raise RuntimeError("Faltan variables de entorno: " + ", ".join(missing))

    url = URL.create(
        "mysql+pymysql",
        username=user,
        password=password,
        host=host,
        port=port,
        database=db,
        query={"charset": "utf8mb4"},
    )

    connect_args = {
        "connect_timeout": 10,
        "read_timeout": 60,
        "write_timeout": 60,
    }
    if ssl_mode not in {"DISABLED", "FALSE", "0", "NO"}:
        # Aiven indica SSL mode REQUIRED. Esto fuerza TLS sin guardar certificados en el repo.
        connect_args["ssl"] = {"check_hostname": False}

    return create_engine(url, pool_pre_ping=True, pool_recycle=280, connect_args=connect_args)


def fetch_scalar(query: str):
    try:
        with get_engine().connect() as conn:
            return conn.execute(text(query)).scalar()
    except Exception:
        return None


def table_count(table_name: str):
    # table_name se valida contra una lista fija antes de llamar esta función.
    return fetch_scalar(f"SELECT COUNT(*) FROM `{table_name}`")


def safe_distinct(column: str, limit: int = 200):
    if column not in {"genero", "dx", "intervencion", "tubo"}:
        return []
    try:
        with get_engine().connect() as conn:
            rows = conn.execute(text(
                f"""
                SELECT DISTINCT `{column}` AS value
                FROM registro_a
                WHERE `{column}` IS NOT NULL AND TRIM(`{column}`) <> ''
                ORDER BY `{column}`
                LIMIT :limit
                """
            ), {"limit": limit}).fetchall()
        return [r[0] for r in rows]
    except Exception:
        return []


@lru_cache(maxsize=1)
def train_random_forest():
    """Entrena el modelo de Random Forest con datos de registro_a.

    RF_LIMIT evita que Render se tarde demasiado o consuma mucha memoria.
    Para entrenar con todos los datos, pon RF_LIMIT vacío o 0 en Render.
    """
    limit = int(get_env("RF_LIMIT", "5000") or "0")
    sql = "SELECT edad, genero, dx, intervencion, tubo FROM registro_a"
    if limit > 0:
        sql += f" LIMIT {limit}"

    df = pd.read_sql(sql, get_engine())
    df = df.replace(r"^\s*$", pd.NA, regex=True).dropna().reset_index(drop=True)
    df["edad"] = pd.to_numeric(df["edad"], errors="coerce")
    df = df.dropna().reset_index(drop=True)

    if len(df) < 5:
        raise RuntimeError("No hay suficientes registros limpios en registro_a para entrenar el modelo.")

    encoders: dict[str, LabelEncoder] = {}
    for col in ["genero", "dx", "intervencion", "tubo"]:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        encoders[col] = le

    X = df[["edad", "genero", "dx", "intervencion"]]
    y = df["tubo"]

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model, encoders, len(df)


def predict_tubo(edad: float, genero: str, dx: str, intervencion: str):
    model, encoders, n_rows = train_random_forest()
    data = pd.DataFrame([{
        "edad": float(edad),
        "genero": genero,
        "dx": dx,
        "intervencion": intervencion,
    }])

    for col in ["genero", "dx", "intervencion"]:
        if data[col].iloc[0] not in encoders[col].classes_:
            valid = list(encoders[col].classes_[:25])
            raise ValueError(
                f"El valor '{data[col].iloc[0]}' no existe en la columna {col}. "
                f"Ejemplos válidos: {valid}"
            )
        data[col] = encoders[col].transform([data[col].iloc[0]])

    pred_num = model.predict(data)[0]
    pred_label = encoders["tubo"].inverse_transform([pred_num])[0]

    proba = None
    if hasattr(model, "predict_proba"):
        classes = model.classes_
        probs = model.predict_proba(data)[0]
        proba = {encoders["tubo"].inverse_transform([cls])[0]: round(float(prob) * 100, 2)
                 for cls, prob in zip(classes, probs)}

    return pred_label, proba, n_rows


def train_linear_model(table: str, x_col: str, y_col: str):
    if table not in {"ventas_historico", "entregas_historico", "backups_historico"}:
        raise ValueError("Tabla no permitida.")
    if x_col not in {"inversion", "distancia_km", "usuarios_miles"}:
        raise ValueError("Columna X no permitida.")
    if y_col not in {"ventas", "tiempo_minutos", "tamano_gb"}:
        raise ValueError("Columna Y no permitida.")

    df = pd.read_sql(f"SELECT `{x_col}`, `{y_col}` FROM `{table}`", get_engine())
    df = df.dropna()
    if len(df) < 2:
        raise RuntimeError(f"No hay suficientes datos en {table}.")

    X = df[[x_col]].astype(float)
    y = df[y_col].astype(float)
    model = LinearRegression()
    model.fit(X, y)
    return model, len(df)


def predict_linear(table: str, x_col: str, y_col: str, value: float):
    model, n_rows = train_linear_model(table, x_col, y_col)
    pred = float(model.predict(pd.DataFrame([{x_col: float(value)}]))[0])
    m = float(model.coef_[0])
    b = float(model.intercept_)
    return pred, m, b, n_rows


@app.route("/")
def index():
    tables = ["registro_a", "ventas_historico", "entregas_historico", "backups_historico"]
    counts = {t: table_count(t) for t in tables}
    db_ok = any(v is not None for v in counts.values())
    return render_template("index.html", counts=counts, db_ok=db_ok)


@app.route("/random-forest", methods=["GET", "POST"])
def random_forest_page():
    result = None
    error = None
    sample = {
        "edad": 68,
        "genero": "Hombre",
        "dx": "COVID 19 POSITIVO",
        "intervencion": "URGENCIAS VALORACIÓN PACIENTES SOSPECHOSOS Y GRAVES POR COVID-19",
    }

    if request.method == "POST":
        try:
            edad = float(request.form.get("edad", "0"))
            genero = request.form.get("genero", "").strip()
            dx = request.form.get("dx", "").strip()
            intervencion = request.form.get("intervencion", "").strip()
            prediction, probabilities, n_rows = predict_tubo(edad, genero, dx, intervencion)
            result = {
                "prediction": prediction,
                "probabilities": probabilities,
                "n_rows": n_rows,
            }
            sample = {"edad": edad, "genero": genero, "dx": dx, "intervencion": intervencion}
        except Exception as exc:
            error = str(exc)

    options = {
        "genero": safe_distinct("genero", 100),
        "dx": safe_distinct("dx", 200),
        "intervencion": safe_distinct("intervencion", 200),
    }
    return render_template("random_forest.html", result=result, error=error, sample=sample, options=options)


@app.route("/probabilidad", methods=["GET", "POST"])
def probabilidad_page():
    scenarios = {
        "ventas": {
            "title": "Predicción de ventas por inversión",
            "table": "ventas_historico",
            "x_col": "inversion",
            "y_col": "ventas",
            "label": "Inversión",
            "unit": "ventas estimadas",
            "default": 25,
        },
        "entregas": {
            "title": "Predicción de tiempo por distancia",
            "table": "entregas_historico",
            "x_col": "distancia_km",
            "y_col": "tiempo_minutos",
            "label": "Distancia en km",
            "unit": "minutos estimados",
            "default": 7,
        },
        "backups": {
            "title": "Predicción de tamaño de respaldo por usuarios",
            "table": "backups_historico",
            "x_col": "usuarios_miles",
            "y_col": "tamano_gb",
            "label": "Usuarios en miles",
            "unit": "GB estimados",
            "default": 5,
        },
    }
    scenario_key = request.form.get("scenario", request.args.get("scenario", "ventas"))
    if scenario_key not in scenarios:
        scenario_key = "ventas"
    scenario = scenarios[scenario_key]

    result = None
    error = None
    input_value = scenario["default"]
    if request.method == "POST":
        try:
            input_value = float(request.form.get("value", scenario["default"]))
            pred, m, b, n_rows = predict_linear(
                scenario["table"], scenario["x_col"], scenario["y_col"], input_value
            )
            result = {
                "prediction": round(pred, 2),
                "m": round(m, 4),
                "b": round(b, 4),
                "n_rows": n_rows,
            }
        except Exception as exc:
            error = str(exc)

    return render_template(
        "probabilidad.html",
        scenarios=scenarios,
        scenario_key=scenario_key,
        scenario=scenario,
        input_value=input_value,
        result=result,
        error=error,
    )


@app.route("/salud")
def health():
    try:
        with get_engine().connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as exc:
        return {"status": "error", "database": str(exc)}, 500


if __name__ == "__main__":
    # Para ejecución local: python app.py
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=True)
