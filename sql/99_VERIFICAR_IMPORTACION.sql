USE `defaultdb`;

SELECT DATABASE() AS base_actual;

SELECT 'ventas_historico' AS tabla, COUNT(*) AS registros FROM ventas_historico
UNION ALL
SELECT 'entregas_historico' AS tabla, COUNT(*) AS registros FROM entregas_historico
UNION ALL
SELECT 'backups_historico' AS tabla, COUNT(*) AS registros FROM backups_historico
UNION ALL
SELECT 'registro_a' AS tabla, COUNT(*) AS registros FROM registro_a;
