# Dashboard Web: Random Forest + Probabilidad/Regresión

Proyecto Flask listo para desplegar en Render y conectarse a una base MySQL administrada en Aiven.

## Módulos

- `/` Dashboard principal.
- `/random-forest` Modelo Random Forest usando la tabla `registro_a`.
- `/probabilidad` Conversión del código C a Python usando regresión lineal.
- `/salud` Prueba de conexión con MySQL/Aiven.

## Base de datos esperada

La app usa una sola base de datos, normalmente `defaultdb`, con estas tablas:

- `registro_a`
- `ventas_historico`
- `entregas_historico`
- `backups_historico`

## Error común de MySQL Workbench

Si aparece:

```text
ERROR 1049 (42000): Unknown database 'Ventas_db_fun'
ERROR 1049 (42000): Unknown database 'c19pruebas'
```

no es error de Aiven ni de la app. Significa que Workbench está intentando importar los dumps con los nombres originales de las bases. Para este proyecto todo debe entrar en `defaultdb`.

Lee primero:

```text
INSTRUCCIONES_CORREGIR_IMPORTACION_AIVEN.md
```

## Importación rápida en Workbench

Ejecuta en una pestaña SQL normal:

```sql
USE defaultdb;
```

Después abre y ejecuta:

```text
sql/00_CREAR_TABLAS_EN_DEFAULTDB.sql
```

Para cargar los datos grandes de Random Forest, limpia el dump original:

```bat
python scripts\preparar_dump_registro_a_para_aiven.py "D:\ruta\c19pruebas_registro_a.sql" "D:\ruta\registro_a_defaultdb.sql"
```

Luego impórtalo:

```bat
mysql --host=TU_HOST_AIVEN --port=TU_PUERTO --user=avnadmin --password --ssl-mode=REQUIRED --database=defaultdb < "D:\ruta\registro_a_defaultdb.sql"
```

## Variables de entorno para Render

Configura estas variables en Render > Environment:

```text
MYSQL_HOST=TU_HOST_AIVEN
MYSQL_PORT=14417
MYSQL_USER=avnadmin
MYSQL_PASSWORD=TU_PASSWORD_AIVEN
MYSQL_DB=defaultdb
MYSQL_SSL_MODE=REQUIRED
RF_LIMIT=5000
```

También puedes usar una sola variable:

```text
MYSQL_URI=mysql://usuario:password@host:puerto/defaultdb?ssl-mode=REQUIRED
```

No subas contraseñas al repositorio.

## Render

Build command:

```text
pip install -r requirements.txt
```

Start command:

```text
gunicorn app:app
```
