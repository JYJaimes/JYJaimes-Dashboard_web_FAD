-- ============================================================
-- IMPORTACIÓN CORRECTA PARA AIVEN
-- Base única: defaultdb
-- Ejecuta este archivo en MySQL Workbench desde una pestaña SQL,
-- NO desde Administration > Data Import/Restore > Dump Project Folder.
-- ============================================================

USE `defaultdb`;

-- Limpieza opcional para poder volver a ejecutar el script sin errores.
DROP TABLE IF EXISTS `ventas_historico`;
DROP TABLE IF EXISTS `entregas_historico`;
DROP TABLE IF EXISTS `backups_historico`;
DROP TABLE IF EXISTS `registro_a`;

-- ============================================================
-- Tablas del módulo de probabilidad / regresión
-- ============================================================

CREATE TABLE `ventas_historico` (
  `id` int NOT NULL AUTO_INCREMENT,
  `mes` varchar(20) DEFAULT NULL,
  `inversion` float DEFAULT NULL,
  `ventas` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `ventas_historico` (`id`, `mes`, `inversion`, `ventas`) VALUES
(1,'Enero',10,50),
(2,'Febrero',20,80),
(3,'Marzo',30,100);

CREATE TABLE `entregas_historico` (
  `id` int NOT NULL AUTO_INCREMENT,
  `distancia_km` float DEFAULT NULL,
  `tiempo_minutos` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `entregas_historico` (`id`, `distancia_km`, `tiempo_minutos`) VALUES
(1,2,12),
(2,4,19),
(3,6,29),
(4,8,37),
(5,10,45);

CREATE TABLE `backups_historico` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuarios_miles` float DEFAULT NULL,
  `tamano_gb` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `backups_historico` (`id`, `usuarios_miles`, `tamano_gb`) VALUES
(1,1,3),
(2,2,5),
(3,3,8),
(4,4,10);

-- ============================================================
-- Tabla del módulo Random Forest
-- IMPORTANTE:
-- Este script solo crea la estructura de registro_a.
-- Después debes importar los datos grandes desde:
-- BD_imss/datos (1)/c19pruebas_registro_a.sql
-- usando el script de limpieza incluido.
-- ============================================================

CREATE TABLE `registro_a` (
  `id_a` int NOT NULL AUTO_INCREMENT,
  `id` int DEFAULT NULL,
  `id_asig` int DEFAULT NULL,
  `id_correc` int DEFAULT NULL,
  `del` varchar(2) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `clp` varchar(12) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `nivel` int DEFAULT NULL,
  `paciente` longtext CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `no_fol` varchar(255) DEFAULT NULL,
  `fecha_derivacion` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `fec_egreso` varchar(255) DEFAULT NULL,
  `nombre` varchar(255) DEFAULT NULL,
  `appat` varchar(255) DEFAULT NULL,
  `apmat` varchar(255) DEFAULT NULL,
  `edad` int DEFAULT NULL,
  `curp` varchar(255) DEFAULT NULL,
  `genero` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `nss` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `dh` varchar(255) DEFAULT NULL,
  `ingreso` varchar(255) DEFAULT NULL,
  `dx` varchar(255) DEFAULT NULL,
  `resclin` longtext DEFAULT NULL,
  `caso` varchar(255) DEFAULT NULL,
  `instituciontraslado` varchar(255) DEFAULT NULL,
  `clues` varchar(255) DEFAULT NULL,
  `hosp_origen` varchar(255) DEFAULT NULL,
  `estado` varchar(255) DEFAULT NULL,
  `municipio` varchar(255) DEFAULT NULL,
  `institucionreceptora` varchar(255) DEFAULT NULL,
  `clues2` varchar(255) DEFAULT NULL,
  `hosp_dest` varchar(255) DEFAULT NULL,
  `delegoumae` varchar(255) DEFAULT NULL,
  `municipio2` varchar(255) DEFAULT NULL,
  `anexo` varchar(10) DEFAULT NULL,
  `codigo` varchar(50) DEFAULT NULL,
  `especialidad` longtext DEFAULT NULL,
  `esp_deriv` longtext DEFAULT NULL,
  `intervencion` longtext DEFAULT NULL,
  `cantidad` int DEFAULT NULL,
  `tarifa` int DEFAULT NULL,
  `fecsis` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `ipconfig` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `nuevos` longtext DEFAULT NULL,
  `marss` varchar(10) DEFAULT NULL,
  `kcovid` varchar(10) DEFAULT NULL,
  `tubo` varchar(10) DEFAULT NULL,
  `fecha_inicio` varchar(255) DEFAULT NULL,
  `fecha_termino` varchar(255) DEFAULT NULL,
  `pdf1` longtext DEFAULT NULL,
  `pdf2` longtext DEFAULT NULL,
  `pdf3` longtext DEFAULT NULL,
  `anexo5` varchar(100) DEFAULT NULL,
  `anexo9` varchar(100) DEFAULT NULL,
  `carga` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id_a`),
  KEY `ida` (`id_a`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SELECT 'Tablas creadas en defaultdb. Ahora importa los datos de registro_a.' AS resultado;
SHOW TABLES;
