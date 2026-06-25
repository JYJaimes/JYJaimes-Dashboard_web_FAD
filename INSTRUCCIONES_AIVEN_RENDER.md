# Instrucciones rápidas: Aiven + Render

## 1. Variables de entorno para Render

En Render > tu Web Service > Environment agrega estas variables.

```text
MYSQL_HOST=mysql-df6f94d-jyjaimes1-889a.g.aivencloud.com
MYSQL_PORT=14417
MYSQL_USER=avnadmin
MYSQL_PASSWORD=PEGA_AQUI_TU_PASSWORD_DE_AIVEN
MYSQL_DB=defaultdb
MYSQL_SSL_MODE=REQUIRED
RF_LIMIT=5000
```

No escribas la contraseña en `app.py`, `README.md`, `.env.example` ni en GitHub.

También puedes usar una sola variable:

```text
MYSQL_URI=mysql://avnadmin:PEGA_AQUI_TU_PASSWORD_DE_AIVEN@mysql-df6f94d-jyjaimes1-889a.g.aivencloud.com:14417/defaultdb?ssl-mode=REQUIRED
```

La app acepta cualquiera de las dos opciones, pero se recomienda usar variables separadas para evitar errores con caracteres especiales en la contraseña.

## 2. Crear tablas en Aiven usando MySQL Workbench

Como ya conectaste Workbench a Aiven, ejecuta los scripts en este orden:

1. `sql/ventas_db_fun.sql`
2. `sql/registro_a_estructura.sql`
3. El dump original grande: `BD_imss/datos (1)/c19pruebas_registro_a.sql`

El archivo 2 crea la estructura de `registro_a`; el archivo 3 mete los datos que usa el Random Forest.

Si el dump grande falla por instrucciones como `LOCK TABLES`, límpialo con:

```bash
python scripts/clean_mysql_dump.py "c19pruebas_registro_a.sql" "registro_a_limpio.sql"
```

Después importa `registro_a_limpio.sql` desde Workbench o terminal.

## 3. Probar conexión local

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Edita `.env` y pega tu contraseña real. Luego:

```bash
python scripts/test_db.py
python app.py
```

Abre `http://localhost:5000`.

## 4. Render

Build Command:

```bash
pip install -r requirements.txt
```

Start Command:

```bash
gunicorn app:app
```

La URL final será algo como:

```text
https://dashboard-randomforest-probabilidad.onrender.com
```
