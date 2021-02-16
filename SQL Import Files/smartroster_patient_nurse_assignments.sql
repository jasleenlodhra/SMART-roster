-- MySQL dump 10.13  Distrib 8.0.21, for Win64 (x86_64)
--
-- Host: localhost    Database: smartroster
-- ------------------------------------------------------
-- Server version	8.0.21

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
-- Table structure for table `nurses`
--

DROP TABLE IF EXISTS `patient_nurse_assignments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;


CREATE TABLE `smartroster`.`patient_nurse_assignments` (
  `assignment_id` INT NOT NULL AUTO_INCREMENT,
  `assignment_shift` DATETIME NOT NULL,
  `frn_nurse_id` INT NULL,
  `frn_patient_id` INT NOT NULL,
  PRIMARY KEY (`assignment_id`));
  
ALTER TABLE `smartroster`.`patient_nurse_assignments` 
ADD INDEX `frn_nurse_id_idx` (`frn_nurse_id` ASC) VISIBLE,
ADD INDEX `assignments_frn_patient_id_idx` (`frn_patient_id` ASC) VISIBLE;
;
ALTER TABLE `smartroster`.`patient_nurse_assignments` 
ADD CONSTRAINT `assignments_frn_nurse_id`
  FOREIGN KEY (`frn_nurse_id`)
  REFERENCES `smartroster`.`nurses` (`id`)
  ON DELETE RESTRICT
  ON UPDATE RESTRICT,
ADD CONSTRAINT `assignments_frn_patient_id`
  FOREIGN KEY (`frn_patient_id`)
  REFERENCES `smartroster`.`patients` (`id`)
  ON DELETE RESTRICT
  ON UPDATE RESTRICT;
