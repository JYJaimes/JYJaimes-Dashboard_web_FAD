# Corrección para Render si se queda en `Preparing metadata (pyproject.toml)`

Este problema aparece durante la instalación de dependencias, antes de que la app intente conectarse a Aiven.
Normalmente significa que Render está usando una versión de Python incompatible con alguna librería científica
(pandas, numpy o scikit-learn) y entonces intenta compilar desde código fuente.

## 1. Agregar versión de Python

Este proyecto ya incluye el archivo:

```txt
.python-version
```

con el contenido:

```txt
3.11.9
```

Además, en Render > Environment agrega o confirma:

```txt
PYTHON_VERSION=3.11.9
```

## 2. Cambiar Build Command

En Render > Settings usa:

```bash
python -m pip install --upgrade pip setuptools wheel && python -m pip install --only-binary=:all: -r requirements.txt
```

Esto evita que Render intente compilar paquetes pesados desde código fuente.

## 3. Cambiar Start Command

En Render > Settings usa:

```bash
gunicorn --bind 0.0.0.0:$PORT app:app
```

## 4. Variables de Aiven

En Render > Environment usa variables, no pegues contraseñas dentro del código:

```txt
MYSQL_HOST=tu-host-de-aiven
MYSQL_PORT=tu-puerto
MYSQL_USER=avnadmin
MYSQL_PASSWORD=tu-password
MYSQL_DB=defaultdb
MYSQL_SSL_MODE=REQUIRED
RF_LIMIT=5000
```

## 5. Redeploy limpio

Después de guardar cambios:

1. Sube `.python-version`, `requirements.txt` y `render.yaml` a GitHub.
2. En Render usa `Clear build cache & deploy`.
3. Revisa `/salud` cuando termine.
