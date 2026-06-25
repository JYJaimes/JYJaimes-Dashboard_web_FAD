# Corrección del error `ERROR 1049 Unknown database`

El error aparece porque MySQL Workbench intentó importar los archivos usando las bases originales del dump:

- `Ventas_db_fun`
- `c19pruebas`

Pero en Aiven solo existe la base `defaultdb`. Para este proyecto NO uses `Administration > Data Import/Restore > Import from Dump Project Folder`, porque Workbench detecta los nombres viejos y ejecuta `--database=Ventas_db_fun` o `--database=c19pruebas`.

## Forma correcta en Workbench

1. Conéctate a Aiven.
2. Abre una pestaña SQL normal.
3. Ejecuta:

```sql
USE defaultdb;
SELECT DATABASE();
```

4. Abre y ejecuta el archivo:

```text
sql/00_CREAR_TABLAS_EN_DEFAULTDB.sql
```

5. Verifica:

```sql
SHOW TABLES;
```

Deben aparecer:

```text
backups_historico
entregas_historico
registro_a
ventas_historico
```

## Importar los datos grandes de Random Forest

Primero crea una versión limpia del dump grande:

```bat
python scripts\preparar_dump_registro_a_para_aiven.py "D:\1. Entregar fundamentos\subir a web\BD_imss\datos (1)\c19pruebas_registro_a.sql" "D:\1. Entregar fundamentos\registro_a_defaultdb.sql"
```

Después impórtalo desde CMD o PowerShell:

```bat
mysql --host=mysql-df6f94d-jyjaimes1-889a.g.aivencloud.com --port=14417 --user=avnadmin --password --ssl-mode=REQUIRED --database=defaultdb < "D:\1. Entregar fundamentos\registro_a_defaultdb.sql"
```

Te va a pedir la contraseña. No la escribas dentro del archivo ni la subas a GitHub.

## Verificación final

Ejecuta:

```sql
USE defaultdb;
SELECT 'ventas_historico' AS tabla, COUNT(*) AS registros FROM ventas_historico
UNION ALL
SELECT 'entregas_historico', COUNT(*) FROM entregas_historico
UNION ALL
SELECT 'backups_historico', COUNT(*) FROM backups_historico
UNION ALL
SELECT 'registro_a', COUNT(*) FROM registro_a;
```
