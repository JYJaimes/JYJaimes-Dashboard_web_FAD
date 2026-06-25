-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: c19pruebas
-- ------------------------------------------------------
-- Server version	5.5.5-10.4.32-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `registro_a`
--

DROP TABLE IF EXISTS `registro_a`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registro_a` (
  `id_a` int(200) NOT NULL AUTO_INCREMENT,
  `id` int(255) DEFAULT NULL,
  `id_asig` int(255) DEFAULT NULL,
  `id_correc` int(255) DEFAULT NULL,
  `del` varchar(2) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `clp` varchar(12) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `nivel` int(10) DEFAULT NULL,
  `paciente` longtext CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `no_fol` varchar(255) DEFAULT NULL,
  `fecha_derivacion` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `fec_egreso` varchar(255) DEFAULT NULL,
  `nombre` varchar(255) DEFAULT NULL,
  `appat` varchar(255) DEFAULT NULL,
  `apmat` varchar(255) DEFAULT NULL,
  `edad` int(11) DEFAULT NULL,
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
  `cantidad` int(100) DEFAULT NULL,
  `tarifa` int(100) DEFAULT NULL,
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
  PRIMARY KEY (`id_a`) USING BTREE,
  KEY `ida` (`id_a`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=583115 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-06-25  0:21:08
