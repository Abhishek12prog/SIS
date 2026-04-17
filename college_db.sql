-- MySQL dump 10.13  Distrib 8.4.0, for macos13.2 (arm64)
--
-- Host: localhost    Database: college_db
-- ------------------------------------------------------
-- Server version	9.6.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `academics`
--

DROP TABLE IF EXISTS `academics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `academics` (
  `id` int NOT NULL AUTO_INCREMENT,
  `student_id` int DEFAULT NULL,
  `subject_name` varchar(100) DEFAULT NULL,
  `internal_marks` int DEFAULT NULL,
  `external_marks` int DEFAULT NULL,
  `total_marks` int DEFAULT NULL,
  `semester` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `student_id` (`student_id`),
  CONSTRAINT `academics_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `academics`
--

LOCK TABLES `academics` WRITE;
/*!40000 ALTER TABLE `academics` DISABLE KEYS */;
INSERT INTO `academics` VALUES (1,1,'Data Structures',25,60,85,'Sem 1'),(2,1,'DBMS',23,55,78,'Sem 1');
/*!40000 ALTER TABLE `academics` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin` (
  `admin_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`admin_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES (1,'admin','admin123');
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `announcements`
--

DROP TABLE IF EXISTS `announcements`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `announcements` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `message` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `announcements`
--

LOCK TABLES `announcements` WRITE;
/*!40000 ALTER TABLE `announcements` DISABLE KEYS */;
INSERT INTO `announcements` VALUES (1,'test 2','','2026-03-18 16:35:35'),(2,'test 2','','2026-03-18 16:35:43'),(3,'test 3','test 3 will start from april 4th','2026-03-18 16:36:02');
/*!40000 ALTER TABLE `announcements` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `branches`
--

DROP TABLE IF EXISTS `branches`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `branches` (
  `id` int NOT NULL AUTO_INCREMENT,
  `branch_name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `branches`
--

LOCK TABLES `branches` WRITE;
/*!40000 ALTER TABLE `branches` DISABLE KEYS */;
INSERT INTO `branches` VALUES (1,'CSE'),(2,'ECE'),(3,'MECH'),(4,'CIVIL');
/*!40000 ALTER TABLE `branches` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `documents`
--

DROP TABLE IF EXISTS `documents`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `documents` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `file_name` varchar(255) DEFAULT NULL,
  `uploaded_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `documents`
--

LOCK TABLES `documents` WRITE;
/*!40000 ALTER TABLE `documents` DISABLE KEYS */;
INSERT INTO `documents` VALUES (1,'lab 1','Lab_3_-_23STUCHH010795_-_G.ABHISHEK.pages','2026-03-18 16:41:24');
/*!40000 ALTER TABLE `documents` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exam_subjects`
--

DROP TABLE IF EXISTS `exam_subjects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `exam_subjects` (
  `id` int NOT NULL AUTO_INCREMENT,
  `student_id` int DEFAULT NULL,
  `subject_name` varchar(100) DEFAULT NULL,
  `exam_date` date DEFAULT NULL,
  `exam_time` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `student_id` (`student_id`),
  CONSTRAINT `exam_subjects_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exam_subjects`
--

LOCK TABLES `exam_subjects` WRITE;
/*!40000 ALTER TABLE `exam_subjects` DISABLE KEYS */;
INSERT INTO `exam_subjects` VALUES (1,1,'Data Structures','2026-03-20','10:00 AM'),(2,1,'DBMS','2026-03-22','2:00 PM');
/*!40000 ALTER TABLE `exam_subjects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feedback`
--

DROP TABLE IF EXISTS `feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feedback` (
  `id` int NOT NULL AUTO_INCREMENT,
  `student_id` int DEFAULT NULL,
  `message` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `student_id` (`student_id`),
  CONSTRAINT `feedback_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feedback`
--

LOCK TABLES `feedback` WRITE;
/*!40000 ALTER TABLE `feedback` DISABLE KEYS */;
/*!40000 ALTER TABLE `feedback` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fees`
--

DROP TABLE IF EXISTS `fees`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fees` (
  `id` int NOT NULL AUTO_INCREMENT,
  `student_id` int DEFAULT NULL,
  `semester` varchar(20) DEFAULT NULL,
  `total_fee` int DEFAULT NULL,
  `paid_amount` int DEFAULT NULL,
  `due_amount` int DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `student_id` (`student_id`),
  CONSTRAINT `fees_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fees`
--

LOCK TABLES `fees` WRITE;
/*!40000 ALTER TABLE `fees` DISABLE KEYS */;
INSERT INTO `fees` VALUES (1,1,'Sem 1',50000,40000,10000,'Pending');
/*!40000 ALTER TABLE `fees` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `helpdesk`
--

DROP TABLE IF EXISTS `helpdesk`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `helpdesk` (
  `id` int NOT NULL AUTO_INCREMENT,
  `student_id` int DEFAULT NULL,
  `subject` varchar(200) DEFAULT NULL,
  `description` text,
  `status` varchar(20) DEFAULT 'Open',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `student_id` (`student_id`),
  CONSTRAINT `helpdesk_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `helpdesk`
--

LOCK TABLES `helpdesk` WRITE;
/*!40000 ALTER TABLE `helpdesk` DISABLE KEYS */;
/*!40000 ALTER TABLE `helpdesk` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notice`
--

DROP TABLE IF EXISTS `notice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notice` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` text,
  `file_name` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `viewed` int DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notice`
--

LOCK TABLES `notice` WRITE;
/*!40000 ALTER TABLE `notice` DISABLE KEYS */;
INSERT INTO `notice` VALUES (1,'Seating Plan','Check your exam seating','seating.pdf','2026-03-24 16:04:49',0);
/*!40000 ALTER TABLE `notice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students` (
  `student_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `branch` varchar(50) DEFAULT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(50) DEFAULT NULL,
  `year` int DEFAULT NULL,
  `semester` int DEFAULT NULL,
  `joining_year` int DEFAULT NULL,
  `course_type` varchar(20) DEFAULT NULL,
  `phone` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`student_id`),
  UNIQUE KEY `uq_students_username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students`
--

LOCK TABLES `students` WRITE;
/*!40000 ALTER TABLE `students` DISABLE KEYS */;
INSERT INTO `students` VALUES
(1,'Aarav Reddy','aarav.reddy.100@gmail.com','CSE','25STUCHH010100','password',1,2,2025,'BTECH','7000000000'),
(2,'Vivaan Sharma','vivaan.sharma.101@gmail.com','CSE','25STUCHH010101','password',1,2,2025,'BTECH','7000000017'),
(3,'Aditya Verma','aditya.verma.102@gmail.com','CSE','25STUCHH010102','password',1,2,2025,'BTECH','7000000034'),
(4,'Vihaan Gupta','vihaan.gupta.103@gmail.com','CSE','25STUCHH010103','password',1,2,2025,'BTECH','7000000051'),
(5,'Arjun Yadav','arjun.yadav.104@gmail.com','CSE','25STUCHH010104','password',1,2,2025,'BTECH','7000000068'),
(6,'Sai Rao','sai.rao.105@gmail.com','CSE','25STUCHH010105','password',1,2,2025,'BTECH','7000000085'),
(7,'Krish Naidu','krish.naidu.106@gmail.com','CSE','25STUCHH010106','password',1,2,2025,'BTECH','7000000102'),
(8,'Ishaan Patel','ishaan.patel.107@gmail.com','CSE','25STUCHH010107','password',1,2,2025,'BTECH','7000000119'),
(9,'Reyansh Kumar','reyansh.kumar.108@gmail.com','CSE','25STUCHH010108','password',1,2,2025,'BTECH','7000000136'),
(10,'Atharv Singh','atharv.singh.109@gmail.com','CSE','25STUCHH010109','password',1,2,2025,'BTECH','7000000153'),
(11,'Nihal Chowdary','nihal.chowdary.110@gmail.com','CSE','25STUCHH010110','password',1,2,2025,'BTECH','7000000170'),
(12,'Rohan Nair','rohan.nair.111@gmail.com','CSE','25STUCHH010111','password',1,2,2025,'BTECH','7000000187'),
(13,'Varun Iyer','varun.iyer.112@gmail.com','CSE','25STUCHH010112','password',1,2,2025,'BTECH','7000000204'),
(14,'Harsha Varma','harsha.varma.113@gmail.com','CSE','25STUCHH010113','password',1,2,2025,'BTECH','7000000221'),
(15,'Karthik Mishra','karthik.mishra.114@gmail.com','CSE','25STUCHH010114','password',1,2,2025,'BTECH','7000000238'),
(16,'Abhinav Pillai','abhinav.pillai.115@gmail.com','CSE','25STUCHH010115','password',1,2,2025,'BTECH','7000000255'),
(17,'Pranav Joshi','pranav.joshi.116@gmail.com','CSE','25STUCHH010116','password',1,2,2025,'BTECH','7000000272'),
(18,'Rahul Goud','rahul.goud.117@gmail.com','CSE','25STUCHH010117','password',1,2,2025,'BTECH','7000000289'),
(19,'Naveen Babu','naveen.babu.118@gmail.com','CSE','25STUCHH010118','password',1,2,2025,'BTECH','7000000306'),
(20,'Manoj Mohan','manoj.mohan.119@gmail.com','CSE','25STUCHH010119','password',1,2,2025,'BTECH','7000000323'),
(21,'Akhil Rani','akhil.rani.120@gmail.com','CSE','25STUCHH010120','password',1,2,2025,'BTECH','7000000340'),
(22,'Tarun Devi','tarun.devi.121@gmail.com','CSE','25STUCHH010121','password',1,2,2025,'BTECH','7000000357'),
(23,'Vivek Sai','vivek.sai.122@gmail.com','CSE','25STUCHH010122','password',1,2,2025,'BTECH','7000000374'),
(24,'Pavan Prasad','pavan.prasad.123@gmail.com','CSE','25STUCHH010123','password',1,2,2025,'BTECH','7000000391'),
(25,'Yash Teja','yash.teja.124@gmail.com','CSE','25STUCHH010124','password',1,2,2025,'BTECH','7000000408'),
(26,'Tejas Kiran','tejas.kiran.125@gmail.com','CSE','25STUCHH010125','password',1,2,2025,'BTECH','7000000425'),
(27,'Ritesh Srinivas','ritesh.srinivas.126@gmail.com','CSE','25STUCHH010126','password',1,2,2025,'BTECH','7000000442'),
(28,'Lokesh Kashyap','lokesh.kashyap.127@gmail.com','CSE','25STUCHH010127','password',1,2,2025,'BTECH','7000000459'),
(29,'Sandeep Reddy','sandeep.reddy.128@gmail.com','CSE','25STUCHH010128','password',1,2,2025,'BTECH','7000000476'),
(30,'Nitin Naik','nitin.naik.129@gmail.com','CSE','25STUCHH010129','password',1,2,2025,'BTECH','7000000493'),
(31,'Ananya Reddy','ananya.reddy.130@gmail.com','CSE','25STUCHH010130','password',1,2,2025,'BTECH','7000000510'),
(32,'Saanvi Sharma','saanvi.sharma.131@gmail.com','CSE','25STUCHH010131','password',1,2,2025,'BTECH','7000000527'),
(33,'Diya Verma','diya.verma.132@gmail.com','CSE','25STUCHH010132','password',1,2,2025,'BTECH','7000000544'),
(34,'Aadhya Gupta','aadhya.gupta.133@gmail.com','CSE','25STUCHH010133','password',1,2,2025,'BTECH','7000000561'),
(35,'Ira Yadav','ira.yadav.134@gmail.com','CSE','25STUCHH010134','password',1,2,2025,'BTECH','7000000578'),
(36,'Myra Rao','myra.rao.135@gmail.com','CSE','25STUCHH010135','password',1,2,2025,'BTECH','7000000595'),
(37,'Kiara Naidu','kiara.naidu.136@gmail.com','CSE','25STUCHH010136','password',1,2,2025,'BTECH','7000000612'),
(38,'Nitya Patel','nitya.patel.137@gmail.com','CSE','25STUCHH010137','password',1,2,2025,'BTECH','7000000629'),
(39,'Ishita Kumar','ishita.kumar.138@gmail.com','CSE','25STUCHH010138','password',1,2,2025,'BTECH','7000000646'),
(40,'Prisha Singh','prisha.singh.139@gmail.com','CSE','25STUCHH010139','password',1,2,2025,'BTECH','7000000663'),
(41,'Meghana Chowdary','meghana.chowdary.140@gmail.com','CSE','25STUCHH010140','password',1,2,2025,'BTECH','7000000680'),
(42,'Harini Nair','harini.nair.141@gmail.com','CSE','25STUCHH010141','password',1,2,2025,'BTECH','7000000697'),
(43,'Sneha Iyer','sneha.iyer.142@gmail.com','CSE','25STUCHH010142','password',1,2,2025,'BTECH','7000000714'),
(44,'Keerthana Varma','keerthana.varma.143@gmail.com','CSE','25STUCHH010143','password',1,2,2025,'BTECH','7000000731'),
(45,'Anvi Mishra','anvi.mishra.144@gmail.com','CSE','25STUCHH010144','password',1,2,2025,'BTECH','7000000748'),
(46,'Ritika Pillai','ritika.pillai.145@gmail.com','CSE','25STUCHH010145','password',1,2,2025,'BTECH','7000000765'),
(47,'Navya Joshi','navya.joshi.146@gmail.com','CSE','25STUCHH010146','password',1,2,2025,'BTECH','7000000782'),
(48,'Deepika Goud','deepika.goud.147@gmail.com','CSE','25STUCHH010147','password',1,2,2025,'BTECH','7000000799'),
(49,'Sravya Babu','sravya.babu.148@gmail.com','CSE','25STUCHH010148','password',1,2,2025,'BTECH','7000000816'),
(50,'Tanvi Mohan','tanvi.mohan.149@gmail.com','CSE','25STUCHH010149','password',1,2,2025,'BTECH','7000000833'),
(51,'Aarav Rani','aarav.rani.150@gmail.com','CSE','25STUCHH010150','password',1,2,2025,'BTECH','7000000850'),
(52,'Vivaan Devi','vivaan.devi.151@gmail.com','CSE','25STUCHH010151','password',1,2,2025,'BTECH','7000000867'),
(53,'Aditya Sai','aditya.sai.152@gmail.com','CSE','25STUCHH010152','password',1,2,2025,'BTECH','7000000884'),
(54,'Vihaan Prasad','vihaan.prasad.153@gmail.com','CSE','25STUCHH010153','password',1,2,2025,'BTECH','7000000901'),
(55,'Arjun Teja','arjun.teja.154@gmail.com','CSE','25STUCHH010154','password',1,2,2025,'BTECH','7000000918'),
(56,'Sai Rani','sai.rani.100@gmail.com','CSEAI','25STUCHH010100','password',1,2,2025,'BTECH','7000000935'),
(57,'Krish Devi','krish.devi.101@gmail.com','CSEAI','25STUCHH010101','password',1,2,2025,'BTECH','7000000952'),
(58,'Ishaan Sai','ishaan.sai.102@gmail.com','CSEAI','25STUCHH010102','password',1,2,2025,'BTECH','7000000969'),
(59,'Reyansh Prasad','reyansh.prasad.103@gmail.com','CSEAI','25STUCHH010103','password',1,2,2025,'BTECH','7000000986'),
(60,'Atharv Teja','atharv.teja.104@gmail.com','CSEAI','25STUCHH010104','password',1,2,2025,'BTECH','7000001003'),
(61,'Nihal Kiran','nihal.kiran.105@gmail.com','CSEAI','25STUCHH010105','password',1,2,2025,'BTECH','7000001020'),
(62,'Rohan Srinivas','rohan.srinivas.106@gmail.com','CSEAI','25STUCHH010106','password',1,2,2025,'BTECH','7000001037'),
(63,'Varun Kashyap','varun.kashyap.107@gmail.com','CSEAI','25STUCHH010107','password',1,2,2025,'BTECH','7000001054'),
(64,'Harsha Reddy','harsha.reddy.108@gmail.com','CSEAI','25STUCHH010108','password',1,2,2025,'BTECH','7000001071'),
(65,'Karthik Naik','karthik.naik.109@gmail.com','CSEAI','25STUCHH010109','password',1,2,2025,'BTECH','7000001088'),
(66,'Abhinav Reddy','abhinav.reddy.110@gmail.com','CSEAI','25STUCHH010110','password',1,2,2025,'BTECH','7000001105'),
(67,'Pranav Sharma','pranav.sharma.111@gmail.com','CSEAI','25STUCHH010111','password',1,2,2025,'BTECH','7000001122'),
(68,'Rahul Verma','rahul.verma.112@gmail.com','CSEAI','25STUCHH010112','password',1,2,2025,'BTECH','7000001139'),
(69,'Naveen Gupta','naveen.gupta.113@gmail.com','CSEAI','25STUCHH010113','password',1,2,2025,'BTECH','7000001156'),
(70,'Manoj Yadav','manoj.yadav.114@gmail.com','CSEAI','25STUCHH010114','password',1,2,2025,'BTECH','7000001173'),
(71,'Akhil Rao','akhil.rao.115@gmail.com','CSEAI','25STUCHH010115','password',1,2,2025,'BTECH','7000001190'),
(72,'Tarun Naidu','tarun.naidu.116@gmail.com','CSEAI','25STUCHH010116','password',1,2,2025,'BTECH','7000001207'),
(73,'Vivek Patel','vivek.patel.117@gmail.com','CSEAI','25STUCHH010117','password',1,2,2025,'BTECH','7000001224'),
(74,'Pavan Kumar','pavan.kumar.118@gmail.com','CSEAI','25STUCHH010118','password',1,2,2025,'BTECH','7000001241'),
(75,'Yash Singh','yash.singh.119@gmail.com','CSEAI','25STUCHH010119','password',1,2,2025,'BTECH','7000001258'),
(76,'Tejas Chowdary','tejas.chowdary.120@gmail.com','CSEAI','25STUCHH010120','password',1,2,2025,'BTECH','7000001275'),
(77,'Ritesh Nair','ritesh.nair.121@gmail.com','CSEAI','25STUCHH010121','password',1,2,2025,'BTECH','7000001292'),
(78,'Lokesh Iyer','lokesh.iyer.122@gmail.com','CSEAI','25STUCHH010122','password',1,2,2025,'BTECH','7000001309'),
(79,'Sandeep Varma','sandeep.varma.123@gmail.com','CSEAI','25STUCHH010123','password',1,2,2025,'BTECH','7000001326'),
(80,'Nitin Mishra','nitin.mishra.124@gmail.com','CSEAI','25STUCHH010124','password',1,2,2025,'BTECH','7000001343'),
(81,'Ananya Pillai','ananya.pillai.125@gmail.com','CSEAI','25STUCHH010125','password',1,2,2025,'BTECH','7000001360'),
(82,'Saanvi Joshi','saanvi.joshi.126@gmail.com','CSEAI','25STUCHH010126','password',1,2,2025,'BTECH','7000001377'),
(83,'Diya Goud','diya.goud.127@gmail.com','CSEAI','25STUCHH010127','password',1,2,2025,'BTECH','7000001394'),
(84,'Aadhya Babu','aadhya.babu.128@gmail.com','CSEAI','25STUCHH010128','password',1,2,2025,'BTECH','7000001411'),
(85,'Ira Mohan','ira.mohan.129@gmail.com','CSEAI','25STUCHH010129','password',1,2,2025,'BTECH','7000001428'),
(86,'Myra Rani','myra.rani.130@gmail.com','CSEAI','25STUCHH010130','password',1,2,2025,'BTECH','7000001445'),
(87,'Kiara Devi','kiara.devi.131@gmail.com','CSEAI','25STUCHH010131','password',1,2,2025,'BTECH','7000001462'),
(88,'Nitya Sai','nitya.sai.132@gmail.com','CSEAI','25STUCHH010132','password',1,2,2025,'BTECH','7000001479'),
(89,'Ishita Prasad','ishita.prasad.133@gmail.com','CSEAI','25STUCHH010133','password',1,2,2025,'BTECH','7000001496'),
(90,'Prisha Teja','prisha.teja.134@gmail.com','CSEAI','25STUCHH010134','password',1,2,2025,'BTECH','7000001513'),
(91,'Meghana Kiran','meghana.kiran.135@gmail.com','CSEAI','25STUCHH010135','password',1,2,2025,'BTECH','7000001530'),
(92,'Harini Srinivas','harini.srinivas.136@gmail.com','CSEAI','25STUCHH010136','password',1,2,2025,'BTECH','7000001547'),
(93,'Sneha Kashyap','sneha.kashyap.137@gmail.com','CSEAI','25STUCHH010137','password',1,2,2025,'BTECH','7000001564'),
(94,'Keerthana Reddy','keerthana.reddy.138@gmail.com','CSEAI','25STUCHH010138','password',1,2,2025,'BTECH','7000001581'),
(95,'Anvi Naik','anvi.naik.139@gmail.com','CSEAI','25STUCHH010139','password',1,2,2025,'BTECH','7000001598'),
(96,'Ritika Reddy','ritika.reddy.140@gmail.com','CSEAI','25STUCHH010140','password',1,2,2025,'BTECH','7000001615'),
(97,'Navya Sharma','navya.sharma.141@gmail.com','CSEAI','25STUCHH010141','password',1,2,2025,'BTECH','7000001632'),
(98,'Deepika Verma','deepika.verma.142@gmail.com','CSEAI','25STUCHH010142','password',1,2,2025,'BTECH','7000001649'),
(99,'Sravya Gupta','sravya.gupta.143@gmail.com','CSEAI','25STUCHH010143','password',1,2,2025,'BTECH','7000001666'),
(100,'Tanvi Yadav','tanvi.yadav.144@gmail.com','CSEAI','25STUCHH010144','password',1,2,2025,'BTECH','7000001683'),
(101,'Aarav Rani','aarav.rani.250@gmail.com','CSE','24STUCHH010250','password',2,4,2024,'BTECH','7000001700'),
(102,'Vivaan Devi','vivaan.devi.251@gmail.com','CSE','24STUCHH010251','password',2,4,2024,'BTECH','7000001717'),
(103,'Aditya Sai','aditya.sai.252@gmail.com','CSE','24STUCHH010252','password',2,4,2024,'BTECH','7000001734'),
(104,'Vihaan Prasad','vihaan.prasad.253@gmail.com','CSE','24STUCHH010253','password',2,4,2024,'BTECH','7000001751'),
(105,'Arjun Teja','arjun.teja.254@gmail.com','CSE','24STUCHH010254','password',2,4,2024,'BTECH','7000001768'),
(106,'Sai Kiran','sai.kiran.255@gmail.com','CSE','24STUCHH010255','password',2,4,2024,'BTECH','7000001785'),
(107,'Krish Srinivas','krish.srinivas.256@gmail.com','CSE','24STUCHH010256','password',2,4,2024,'BTECH','7000001802'),
(108,'Ishaan Kashyap','ishaan.kashyap.257@gmail.com','CSE','24STUCHH010257','password',2,4,2024,'BTECH','7000001819'),
(109,'Reyansh Reddy','reyansh.reddy.258@gmail.com','CSE','24STUCHH010258','password',2,4,2024,'BTECH','7000001836'),
(110,'Atharv Naik','atharv.naik.259@gmail.com','CSE','24STUCHH010259','password',2,4,2024,'BTECH','7000001853'),
(111,'Nihal Reddy','nihal.reddy.260@gmail.com','CSE','24STUCHH010260','password',2,4,2024,'BTECH','7000001870'),
(112,'Rohan Sharma','rohan.sharma.261@gmail.com','CSE','24STUCHH010261','password',2,4,2024,'BTECH','7000001887'),
(113,'Varun Verma','varun.verma.262@gmail.com','CSE','24STUCHH010262','password',2,4,2024,'BTECH','7000001904'),
(114,'Harsha Gupta','harsha.gupta.263@gmail.com','CSE','24STUCHH010263','password',2,4,2024,'BTECH','7000001921'),
(115,'Karthik Yadav','karthik.yadav.264@gmail.com','CSE','24STUCHH010264','password',2,4,2024,'BTECH','7000001938'),
(116,'Abhinav Rao','abhinav.rao.265@gmail.com','CSE','24STUCHH010265','password',2,4,2024,'BTECH','7000001955'),
(117,'Pranav Naidu','pranav.naidu.266@gmail.com','CSE','24STUCHH010266','password',2,4,2024,'BTECH','7000001972'),
(118,'Rahul Patel','rahul.patel.267@gmail.com','CSE','24STUCHH010267','password',2,4,2024,'BTECH','7000001989'),
(119,'Naveen Kumar','naveen.kumar.268@gmail.com','CSE','24STUCHH010268','password',2,4,2024,'BTECH','7000002006'),
(120,'Manoj Singh','manoj.singh.269@gmail.com','CSE','24STUCHH010269','password',2,4,2024,'BTECH','7000002023'),
(121,'Akhil Chowdary','akhil.chowdary.270@gmail.com','CSE','24STUCHH010270','password',2,4,2024,'BTECH','7000002040'),
(122,'Tarun Nair','tarun.nair.271@gmail.com','CSE','24STUCHH010271','password',2,4,2024,'BTECH','7000002057'),
(123,'Vivek Iyer','vivek.iyer.272@gmail.com','CSE','24STUCHH010272','password',2,4,2024,'BTECH','7000002074'),
(124,'Pavan Varma','pavan.varma.273@gmail.com','CSE','24STUCHH010273','password',2,4,2024,'BTECH','7000002091'),
(125,'Yash Mishra','yash.mishra.274@gmail.com','CSE','24STUCHH010274','password',2,4,2024,'BTECH','7000002108'),
(126,'Tejas Pillai','tejas.pillai.275@gmail.com','CSE','24STUCHH010275','password',2,4,2024,'BTECH','7000002125'),
(127,'Ritesh Joshi','ritesh.joshi.276@gmail.com','CSE','24STUCHH010276','password',2,4,2024,'BTECH','7000002142'),
(128,'Lokesh Goud','lokesh.goud.277@gmail.com','CSE','24STUCHH010277','password',2,4,2024,'BTECH','7000002159'),
(129,'Sandeep Babu','sandeep.babu.278@gmail.com','CSE','24STUCHH010278','password',2,4,2024,'BTECH','7000002176'),
(130,'Nitin Mohan','nitin.mohan.279@gmail.com','CSE','24STUCHH010279','password',2,4,2024,'BTECH','7000002193'),
(131,'Ananya Rani','ananya.rani.280@gmail.com','CSE','24STUCHH010280','password',2,4,2024,'BTECH','7000002210'),
(132,'Saanvi Devi','saanvi.devi.281@gmail.com','CSE','24STUCHH010281','password',2,4,2024,'BTECH','7000002227'),
(133,'Diya Sai','diya.sai.282@gmail.com','CSE','24STUCHH010282','password',2,4,2024,'BTECH','7000002244'),
(134,'Aadhya Prasad','aadhya.prasad.283@gmail.com','CSE','24STUCHH010283','password',2,4,2024,'BTECH','7000002261'),
(135,'Ira Teja','ira.teja.284@gmail.com','CSE','24STUCHH010284','password',2,4,2024,'BTECH','7000002278'),
(136,'Myra Kiran','myra.kiran.285@gmail.com','CSE','24STUCHH010285','password',2,4,2024,'BTECH','7000002295'),
(137,'Kiara Srinivas','kiara.srinivas.286@gmail.com','CSE','24STUCHH010286','password',2,4,2024,'BTECH','7000002312'),
(138,'Nitya Kashyap','nitya.kashyap.287@gmail.com','CSE','24STUCHH010287','password',2,4,2024,'BTECH','7000002329'),
(139,'Ishita Reddy','ishita.reddy.288@gmail.com','CSE','24STUCHH010288','password',2,4,2024,'BTECH','7000002346'),
(140,'Prisha Naik','prisha.naik.289@gmail.com','CSE','24STUCHH010289','password',2,4,2024,'BTECH','7000002363'),
(141,'Meghana Reddy','meghana.reddy.290@gmail.com','CSE','24STUCHH010290','password',2,4,2024,'BTECH','7000002380'),
(142,'Harini Sharma','harini.sharma.291@gmail.com','CSE','24STUCHH010291','password',2,4,2024,'BTECH','7000002397'),
(143,'Sneha Verma','sneha.verma.292@gmail.com','CSE','24STUCHH010292','password',2,4,2024,'BTECH','7000002414'),
(144,'Keerthana Gupta','keerthana.gupta.293@gmail.com','CSE','24STUCHH010293','password',2,4,2024,'BTECH','7000002431'),
(145,'Anvi Yadav','anvi.yadav.294@gmail.com','CSE','24STUCHH010294','password',2,4,2024,'BTECH','7000002448'),
(146,'Ritika Rao','ritika.rao.295@gmail.com','CSE','24STUCHH010295','password',2,4,2024,'BTECH','7000002465'),
(147,'Navya Naidu','navya.naidu.296@gmail.com','CSE','24STUCHH010296','password',2,4,2024,'BTECH','7000002482'),
(148,'Deepika Patel','deepika.patel.297@gmail.com','CSE','24STUCHH010297','password',2,4,2024,'BTECH','7000002499'),
(149,'Sravya Kumar','sravya.kumar.298@gmail.com','CSE','24STUCHH010298','password',2,4,2024,'BTECH','7000002516'),
(150,'Tanvi Singh','tanvi.singh.299@gmail.com','CSE','24STUCHH010299','password',2,4,2024,'BTECH','7000002533'),
(151,'Aarav Chowdary','aarav.chowdary.300@gmail.com','CSE','24STUCHH010300','password',2,4,2024,'BTECH','7000002550'),
(152,'Vivaan Nair','vivaan.nair.301@gmail.com','CSE','24STUCHH010301','password',2,4,2024,'BTECH','7000002567'),
(153,'Aditya Iyer','aditya.iyer.302@gmail.com','CSE','24STUCHH010302','password',2,4,2024,'BTECH','7000002584'),
(154,'Vihaan Varma','vihaan.varma.303@gmail.com','CSE','24STUCHH010303','password',2,4,2024,'BTECH','7000002601'),
(155,'Arjun Mishra','arjun.mishra.304@gmail.com','CSE','24STUCHH010304','password',2,4,2024,'BTECH','7000002618'),
(156,'Sai Chowdary','sai.chowdary.250@gmail.com','CSEDS','24STUCHH010250','password',2,4,2024,'BTECH','7000002635'),
(157,'Krish Nair','krish.nair.251@gmail.com','CSEDS','24STUCHH010251','password',2,4,2024,'BTECH','7000002652'),
(158,'Ishaan Iyer','ishaan.iyer.252@gmail.com','CSEDS','24STUCHH010252','password',2,4,2024,'BTECH','7000002669'),
(159,'Reyansh Varma','reyansh.varma.253@gmail.com','CSEDS','24STUCHH010253','password',2,4,2024,'BTECH','7000002686'),
(160,'Atharv Mishra','atharv.mishra.254@gmail.com','CSEDS','24STUCHH010254','password',2,4,2024,'BTECH','7000002703'),
(161,'Nihal Pillai','nihal.pillai.255@gmail.com','CSEDS','24STUCHH010255','password',2,4,2024,'BTECH','7000002720'),
(162,'Rohan Joshi','rohan.joshi.256@gmail.com','CSEDS','24STUCHH010256','password',2,4,2024,'BTECH','7000002737'),
(163,'Varun Goud','varun.goud.257@gmail.com','CSEDS','24STUCHH010257','password',2,4,2024,'BTECH','7000002754'),
(164,'Harsha Babu','harsha.babu.258@gmail.com','CSEDS','24STUCHH010258','password',2,4,2024,'BTECH','7000002771'),
(165,'Karthik Mohan','karthik.mohan.259@gmail.com','CSEDS','24STUCHH010259','password',2,4,2024,'BTECH','7000002788'),
(166,'Abhinav Rani','abhinav.rani.260@gmail.com','CSEDS','24STUCHH010260','password',2,4,2024,'BTECH','7000002805'),
(167,'Pranav Devi','pranav.devi.261@gmail.com','CSEDS','24STUCHH010261','password',2,4,2024,'BTECH','7000002822'),
(168,'Rahul Sai','rahul.sai.262@gmail.com','CSEDS','24STUCHH010262','password',2,4,2024,'BTECH','7000002839'),
(169,'Naveen Prasad','naveen.prasad.263@gmail.com','CSEDS','24STUCHH010263','password',2,4,2024,'BTECH','7000002856'),
(170,'Manoj Teja','manoj.teja.264@gmail.com','CSEDS','24STUCHH010264','password',2,4,2024,'BTECH','7000002873'),
(171,'Akhil Kiran','akhil.kiran.265@gmail.com','CSEDS','24STUCHH010265','password',2,4,2024,'BTECH','7000002890'),
(172,'Tarun Srinivas','tarun.srinivas.266@gmail.com','CSEDS','24STUCHH010266','password',2,4,2024,'BTECH','7000002907'),
(173,'Vivek Kashyap','vivek.kashyap.267@gmail.com','CSEDS','24STUCHH010267','password',2,4,2024,'BTECH','7000002924'),
(174,'Pavan Reddy','pavan.reddy.268@gmail.com','CSEDS','24STUCHH010268','password',2,4,2024,'BTECH','7000002941'),
(175,'Yash Naik','yash.naik.269@gmail.com','CSEDS','24STUCHH010269','password',2,4,2024,'BTECH','7000002958'),
(176,'Tejas Reddy','tejas.reddy.270@gmail.com','CSEDS','24STUCHH010270','password',2,4,2024,'BTECH','7000002975'),
(177,'Ritesh Sharma','ritesh.sharma.271@gmail.com','CSEDS','24STUCHH010271','password',2,4,2024,'BTECH','7000002992'),
(178,'Lokesh Verma','lokesh.verma.272@gmail.com','CSEDS','24STUCHH010272','password',2,4,2024,'BTECH','7000003009'),
(179,'Sandeep Gupta','sandeep.gupta.273@gmail.com','CSEDS','24STUCHH010273','password',2,4,2024,'BTECH','7000003026'),
(180,'Nitin Yadav','nitin.yadav.274@gmail.com','CSEDS','24STUCHH010274','password',2,4,2024,'BTECH','7000003043'),
(181,'Ananya Rao','ananya.rao.275@gmail.com','CSEDS','24STUCHH010275','password',2,4,2024,'BTECH','7000003060'),
(182,'Saanvi Naidu','saanvi.naidu.276@gmail.com','CSEDS','24STUCHH010276','password',2,4,2024,'BTECH','7000003077'),
(183,'Diya Patel','diya.patel.277@gmail.com','CSEDS','24STUCHH010277','password',2,4,2024,'BTECH','7000003094'),
(184,'Aadhya Kumar','aadhya.kumar.278@gmail.com','CSEDS','24STUCHH010278','password',2,4,2024,'BTECH','7000003111'),
(185,'Ira Singh','ira.singh.279@gmail.com','CSEDS','24STUCHH010279','password',2,4,2024,'BTECH','7000003128'),
(186,'Myra Chowdary','myra.chowdary.280@gmail.com','CSEDS','24STUCHH010280','password',2,4,2024,'BTECH','7000003145'),
(187,'Kiara Nair','kiara.nair.281@gmail.com','CSEDS','24STUCHH010281','password',2,4,2024,'BTECH','7000003162'),
(188,'Nitya Iyer','nitya.iyer.282@gmail.com','CSEDS','24STUCHH010282','password',2,4,2024,'BTECH','7000003179'),
(189,'Ishita Varma','ishita.varma.283@gmail.com','CSEDS','24STUCHH010283','password',2,4,2024,'BTECH','7000003196'),
(190,'Prisha Mishra','prisha.mishra.284@gmail.com','CSEDS','24STUCHH010284','password',2,4,2024,'BTECH','7000003213'),
(191,'Meghana Pillai','meghana.pillai.285@gmail.com','CSEDS','24STUCHH010285','password',2,4,2024,'BTECH','7000003230'),
(192,'Harini Joshi','harini.joshi.286@gmail.com','CSEDS','24STUCHH010286','password',2,4,2024,'BTECH','7000003247'),
(193,'Sneha Goud','sneha.goud.287@gmail.com','CSEDS','24STUCHH010287','password',2,4,2024,'BTECH','7000003264'),
(194,'Keerthana Babu','keerthana.babu.288@gmail.com','CSEDS','24STUCHH010288','password',2,4,2024,'BTECH','7000003281'),
(195,'Anvi Mohan','anvi.mohan.289@gmail.com','CSEDS','24STUCHH010289','password',2,4,2024,'BTECH','7000003298'),
(196,'Ritika Rani','ritika.rani.290@gmail.com','CSEDS','24STUCHH010290','password',2,4,2024,'BTECH','7000003315'),
(197,'Navya Devi','navya.devi.291@gmail.com','CSEDS','24STUCHH010291','password',2,4,2024,'BTECH','7000003332'),
(198,'Deepika Sai','deepika.sai.292@gmail.com','CSEDS','24STUCHH010292','password',2,4,2024,'BTECH','7000003349'),
(199,'Sravya Prasad','sravya.prasad.293@gmail.com','CSEDS','24STUCHH010293','password',2,4,2024,'BTECH','7000003366'),
(200,'Tanvi Teja','tanvi.teja.294@gmail.com','CSEDS','24STUCHH010294','password',2,4,2024,'BTECH','7000003383'),
(201,'Aarav Chowdary','aarav.chowdary.500@gmail.com','ECE','23STUCHH010500','password',3,6,2023,'BTECH','7000003400'),
(202,'Vivaan Nair','vivaan.nair.501@gmail.com','ECE','23STUCHH010501','password',3,6,2023,'BTECH','7000003417'),
(203,'Aditya Iyer','aditya.iyer.502@gmail.com','ECE','23STUCHH010502','password',3,6,2023,'BTECH','7000003434'),
(204,'Vihaan Varma','vihaan.varma.503@gmail.com','ECE','23STUCHH010503','password',3,6,2023,'BTECH','7000003451'),
(205,'Arjun Mishra','arjun.mishra.504@gmail.com','ECE','23STUCHH010504','password',3,6,2023,'BTECH','7000003468'),
(206,'Sai Pillai','sai.pillai.505@gmail.com','ECE','23STUCHH010505','password',3,6,2023,'BTECH','7000003485'),
(207,'Krish Joshi','krish.joshi.506@gmail.com','ECE','23STUCHH010506','password',3,6,2023,'BTECH','7000003502'),
(208,'Ishaan Goud','ishaan.goud.507@gmail.com','ECE','23STUCHH010507','password',3,6,2023,'BTECH','7000003519'),
(209,'Reyansh Babu','reyansh.babu.508@gmail.com','ECE','23STUCHH010508','password',3,6,2023,'BTECH','7000003536'),
(210,'Atharv Mohan','atharv.mohan.509@gmail.com','ECE','23STUCHH010509','password',3,6,2023,'BTECH','7000003553'),
(211,'Nihal Rani','nihal.rani.510@gmail.com','ECE','23STUCHH010510','password',3,6,2023,'BTECH','7000003570'),
(212,'Rohan Devi','rohan.devi.511@gmail.com','ECE','23STUCHH010511','password',3,6,2023,'BTECH','7000003587'),
(213,'Varun Sai','varun.sai.512@gmail.com','ECE','23STUCHH010512','password',3,6,2023,'BTECH','7000003604'),
(214,'Harsha Prasad','harsha.prasad.513@gmail.com','ECE','23STUCHH010513','password',3,6,2023,'BTECH','7000003621'),
(215,'Karthik Teja','karthik.teja.514@gmail.com','ECE','23STUCHH010514','password',3,6,2023,'BTECH','7000003638'),
(216,'Abhinav Kiran','abhinav.kiran.515@gmail.com','ECE','23STUCHH010515','password',3,6,2023,'BTECH','7000003655'),
(217,'Pranav Srinivas','pranav.srinivas.516@gmail.com','ECE','23STUCHH010516','password',3,6,2023,'BTECH','7000003672'),
(218,'Rahul Kashyap','rahul.kashyap.517@gmail.com','ECE','23STUCHH010517','password',3,6,2023,'BTECH','7000003689'),
(219,'Naveen Reddy','naveen.reddy.518@gmail.com','ECE','23STUCHH010518','password',3,6,2023,'BTECH','7000003706'),
(220,'Manoj Naik','manoj.naik.519@gmail.com','ECE','23STUCHH010519','password',3,6,2023,'BTECH','7000003723'),
(221,'Akhil Reddy','akhil.reddy.520@gmail.com','ECE','23STUCHH010520','password',3,6,2023,'BTECH','7000003740'),
(222,'Tarun Sharma','tarun.sharma.521@gmail.com','ECE','23STUCHH010521','password',3,6,2023,'BTECH','7000003757'),
(223,'Vivek Verma','vivek.verma.522@gmail.com','ECE','23STUCHH010522','password',3,6,2023,'BTECH','7000003774'),
(224,'Pavan Gupta','pavan.gupta.523@gmail.com','ECE','23STUCHH010523','password',3,6,2023,'BTECH','7000003791'),
(225,'Yash Yadav','yash.yadav.524@gmail.com','ECE','23STUCHH010524','password',3,6,2023,'BTECH','7000003808'),
(226,'Tejas Rao','tejas.rao.525@gmail.com','ECE','23STUCHH010525','password',3,6,2023,'BTECH','7000003825'),
(227,'Ritesh Naidu','ritesh.naidu.526@gmail.com','ECE','23STUCHH010526','password',3,6,2023,'BTECH','7000003842'),
(228,'Lokesh Patel','lokesh.patel.527@gmail.com','ECE','23STUCHH010527','password',3,6,2023,'BTECH','7000003859'),
(229,'Sandeep Kumar','sandeep.kumar.528@gmail.com','ECE','23STUCHH010528','password',3,6,2023,'BTECH','7000003876'),
(230,'Nitin Singh','nitin.singh.529@gmail.com','ECE','23STUCHH010529','password',3,6,2023,'BTECH','7000003893'),
(231,'Ananya Chowdary','ananya.chowdary.530@gmail.com','ECE','23STUCHH010530','password',3,6,2023,'BTECH','7000003910'),
(232,'Saanvi Nair','saanvi.nair.531@gmail.com','ECE','23STUCHH010531','password',3,6,2023,'BTECH','7000003927'),
(233,'Diya Iyer','diya.iyer.532@gmail.com','ECE','23STUCHH010532','password',3,6,2023,'BTECH','7000003944'),
(234,'Aadhya Varma','aadhya.varma.533@gmail.com','ECE','23STUCHH010533','password',3,6,2023,'BTECH','7000003961'),
(235,'Ira Mishra','ira.mishra.534@gmail.com','ECE','23STUCHH010534','password',3,6,2023,'BTECH','7000003978'),
(236,'Myra Pillai','myra.pillai.535@gmail.com','ECE','23STUCHH010535','password',3,6,2023,'BTECH','7000003995'),
(237,'Kiara Joshi','kiara.joshi.536@gmail.com','ECE','23STUCHH010536','password',3,6,2023,'BTECH','7000004012'),
(238,'Nitya Goud','nitya.goud.537@gmail.com','ECE','23STUCHH010537','password',3,6,2023,'BTECH','7000004029'),
(239,'Ishita Babu','ishita.babu.538@gmail.com','ECE','23STUCHH010538','password',3,6,2023,'BTECH','7000004046'),
(240,'Prisha Mohan','prisha.mohan.539@gmail.com','ECE','23STUCHH010539','password',3,6,2023,'BTECH','7000004063'),
(241,'Meghana Rani','meghana.rani.540@gmail.com','ECE','23STUCHH010540','password',3,6,2023,'BTECH','7000004080'),
(242,'Harini Devi','harini.devi.541@gmail.com','ECE','23STUCHH010541','password',3,6,2023,'BTECH','7000004097'),
(243,'Sneha Sai','sneha.sai.542@gmail.com','ECE','23STUCHH010542','password',3,6,2023,'BTECH','7000004114'),
(244,'Keerthana Prasad','keerthana.prasad.543@gmail.com','ECE','23STUCHH010543','password',3,6,2023,'BTECH','7000004131'),
(245,'Anvi Teja','anvi.teja.544@gmail.com','ECE','23STUCHH010544','password',3,6,2023,'BTECH','7000004148'),
(246,'Ritika Kiran','ritika.kiran.545@gmail.com','ECE','23STUCHH010545','password',3,6,2023,'BTECH','7000004165'),
(247,'Navya Srinivas','navya.srinivas.546@gmail.com','ECE','23STUCHH010546','password',3,6,2023,'BTECH','7000004182'),
(248,'Deepika Kashyap','deepika.kashyap.547@gmail.com','ECE','23STUCHH010547','password',3,6,2023,'BTECH','7000004199'),
(249,'Sravya Reddy','sravya.reddy.548@gmail.com','ECE','23STUCHH010548','password',3,6,2023,'BTECH','7000004216'),
(250,'Tanvi Naik','tanvi.naik.549@gmail.com','ECE','23STUCHH010549','password',3,6,2023,'BTECH','7000004233'),
(251,'Aarav Reddy','aarav.reddy.550@gmail.com','ECE','23STUCHH010550','password',3,6,2023,'BTECH','7000004250'),
(252,'Vivaan Sharma','vivaan.sharma.551@gmail.com','ECE','23STUCHH010551','password',3,6,2023,'BTECH','7000004267'),
(253,'Aditya Verma','aditya.verma.552@gmail.com','ECE','23STUCHH010552','password',3,6,2023,'BTECH','7000004284'),
(254,'Vihaan Gupta','vihaan.gupta.553@gmail.com','ECE','23STUCHH010553','password',3,6,2023,'BTECH','7000004301'),
(255,'Arjun Yadav','arjun.yadav.554@gmail.com','ECE','23STUCHH010554','password',3,6,2023,'BTECH','7000004318'),
(256,'Sai Reddy','sai.reddy.500@gmail.com','CSE','23STUCHH010500','password',3,6,2023,'BTECH','7000004335'),
(257,'Krish Sharma','krish.sharma.501@gmail.com','CSE','23STUCHH010501','password',3,6,2023,'BTECH','7000004352'),
(258,'Ishaan Verma','ishaan.verma.502@gmail.com','CSE','23STUCHH010502','password',3,6,2023,'BTECH','7000004369'),
(259,'Reyansh Gupta','reyansh.gupta.503@gmail.com','CSE','23STUCHH010503','password',3,6,2023,'BTECH','7000004386'),
(260,'Atharv Yadav','atharv.yadav.504@gmail.com','CSE','23STUCHH010504','password',3,6,2023,'BTECH','7000004403'),
(261,'Nihal Rao','nihal.rao.505@gmail.com','CSE','23STUCHH010505','password',3,6,2023,'BTECH','7000004420'),
(262,'Rohan Naidu','rohan.naidu.506@gmail.com','CSE','23STUCHH010506','password',3,6,2023,'BTECH','7000004437'),
(263,'Varun Patel','varun.patel.507@gmail.com','CSE','23STUCHH010507','password',3,6,2023,'BTECH','7000004454'),
(264,'Harsha Kumar','harsha.kumar.508@gmail.com','CSE','23STUCHH010508','password',3,6,2023,'BTECH','7000004471'),
(265,'Karthik Singh','karthik.singh.509@gmail.com','CSE','23STUCHH010509','password',3,6,2023,'BTECH','7000004488'),
(266,'Abhinav Chowdary','abhinav.chowdary.510@gmail.com','CSE','23STUCHH010510','password',3,6,2023,'BTECH','7000004505'),
(267,'Pranav Nair','pranav.nair.511@gmail.com','CSE','23STUCHH010511','password',3,6,2023,'BTECH','7000004522'),
(268,'Rahul Iyer','rahul.iyer.512@gmail.com','CSE','23STUCHH010512','password',3,6,2023,'BTECH','7000004539'),
(269,'Naveen Varma','naveen.varma.513@gmail.com','CSE','23STUCHH010513','password',3,6,2023,'BTECH','7000004556'),
(270,'Manoj Mishra','manoj.mishra.514@gmail.com','CSE','23STUCHH010514','password',3,6,2023,'BTECH','7000004573'),
(271,'Akhil Pillai','akhil.pillai.515@gmail.com','CSE','23STUCHH010515','password',3,6,2023,'BTECH','7000004590'),
(272,'Tarun Joshi','tarun.joshi.516@gmail.com','CSE','23STUCHH010516','password',3,6,2023,'BTECH','7000004607'),
(273,'Vivek Goud','vivek.goud.517@gmail.com','CSE','23STUCHH010517','password',3,6,2023,'BTECH','7000004624'),
(274,'Pavan Babu','pavan.babu.518@gmail.com','CSE','23STUCHH010518','password',3,6,2023,'BTECH','7000004641'),
(275,'Yash Mohan','yash.mohan.519@gmail.com','CSE','23STUCHH010519','password',3,6,2023,'BTECH','7000004658'),
(276,'Tejas Rani','tejas.rani.520@gmail.com','CSE','23STUCHH010520','password',3,6,2023,'BTECH','7000004675'),
(277,'Ritesh Devi','ritesh.devi.521@gmail.com','CSE','23STUCHH010521','password',3,6,2023,'BTECH','7000004692'),
(278,'Lokesh Sai','lokesh.sai.522@gmail.com','CSE','23STUCHH010522','password',3,6,2023,'BTECH','7000004709'),
(279,'Sandeep Prasad','sandeep.prasad.523@gmail.com','CSE','23STUCHH010523','password',3,6,2023,'BTECH','7000004726'),
(280,'Nitin Teja','nitin.teja.524@gmail.com','CSE','23STUCHH010524','password',3,6,2023,'BTECH','7000004743'),
(281,'Ananya Kiran','ananya.kiran.525@gmail.com','CSE','23STUCHH010525','password',3,6,2023,'BTECH','7000004760'),
(282,'Saanvi Srinivas','saanvi.srinivas.526@gmail.com','CSE','23STUCHH010526','password',3,6,2023,'BTECH','7000004777'),
(283,'Diya Kashyap','diya.kashyap.527@gmail.com','CSE','23STUCHH010527','password',3,6,2023,'BTECH','7000004794'),
(284,'Aadhya Reddy','aadhya.reddy.528@gmail.com','CSE','23STUCHH010528','password',3,6,2023,'BTECH','7000004811'),
(285,'Ira Naik','ira.naik.529@gmail.com','CSE','23STUCHH010529','password',3,6,2023,'BTECH','7000004828'),
(286,'Myra Reddy','myra.reddy.530@gmail.com','CSE','23STUCHH010530','password',3,6,2023,'BTECH','7000004845'),
(287,'Kiara Sharma','kiara.sharma.531@gmail.com','CSE','23STUCHH010531','password',3,6,2023,'BTECH','7000004862'),
(288,'Nitya Verma','nitya.verma.532@gmail.com','CSE','23STUCHH010532','password',3,6,2023,'BTECH','7000004879'),
(289,'Ishita Gupta','ishita.gupta.533@gmail.com','CSE','23STUCHH010533','password',3,6,2023,'BTECH','7000004896'),
(290,'Prisha Yadav','prisha.yadav.534@gmail.com','CSE','23STUCHH010534','password',3,6,2023,'BTECH','7000004913'),
(291,'Meghana Rao','meghana.rao.535@gmail.com','CSE','23STUCHH010535','password',3,6,2023,'BTECH','7000004930'),
(292,'Harini Naidu','harini.naidu.536@gmail.com','CSE','23STUCHH010536','password',3,6,2023,'BTECH','7000004947'),
(293,'Sneha Patel','sneha.patel.537@gmail.com','CSE','23STUCHH010537','password',3,6,2023,'BTECH','7000004964'),
(294,'Keerthana Kumar','keerthana.kumar.538@gmail.com','CSE','23STUCHH010538','password',3,6,2023,'BTECH','7000004981'),
(295,'Anvi Singh','anvi.singh.539@gmail.com','CSE','23STUCHH010539','password',3,6,2023,'BTECH','7000004998'),
(296,'Ritika Chowdary','ritika.chowdary.540@gmail.com','CSE','23STUCHH010540','password',3,6,2023,'BTECH','7000005015'),
(297,'Navya Nair','navya.nair.541@gmail.com','CSE','23STUCHH010541','password',3,6,2023,'BTECH','7000005032'),
(298,'Deepika Iyer','deepika.iyer.542@gmail.com','CSE','23STUCHH010542','password',3,6,2023,'BTECH','7000005049'),
(299,'Sravya Varma','sravya.varma.543@gmail.com','CSE','23STUCHH010543','password',3,6,2023,'BTECH','7000005066'),
(300,'Tanvi Mishra','tanvi.mishra.544@gmail.com','CSE','23STUCHH010544','password',3,6,2023,'BTECH','7000005083'),
(301,'Aarav Reddy','aarav.reddy.750@gmail.com','ECE','22STUCHH010750','password',4,8,2022,'BTECH','7000005100'),
(302,'Vivaan Sharma','vivaan.sharma.751@gmail.com','ECE','22STUCHH010751','password',4,8,2022,'BTECH','7000005117'),
(303,'Aditya Verma','aditya.verma.752@gmail.com','ECE','22STUCHH010752','password',4,8,2022,'BTECH','7000005134'),
(304,'Vihaan Gupta','vihaan.gupta.753@gmail.com','ECE','22STUCHH010753','password',4,8,2022,'BTECH','7000005151'),
(305,'Arjun Yadav','arjun.yadav.754@gmail.com','ECE','22STUCHH010754','password',4,8,2022,'BTECH','7000005168'),
(306,'Sai Rao','sai.rao.755@gmail.com','ECE','22STUCHH010755','password',4,8,2022,'BTECH','7000005185'),
(307,'Krish Naidu','krish.naidu.756@gmail.com','ECE','22STUCHH010756','password',4,8,2022,'BTECH','7000005202'),
(308,'Ishaan Patel','ishaan.patel.757@gmail.com','ECE','22STUCHH010757','password',4,8,2022,'BTECH','7000005219'),
(309,'Reyansh Kumar','reyansh.kumar.758@gmail.com','ECE','22STUCHH010758','password',4,8,2022,'BTECH','7000005236'),
(310,'Atharv Singh','atharv.singh.759@gmail.com','ECE','22STUCHH010759','password',4,8,2022,'BTECH','7000005253'),
(311,'Nihal Chowdary','nihal.chowdary.760@gmail.com','ECE','22STUCHH010760','password',4,8,2022,'BTECH','7000005270'),
(312,'Rohan Nair','rohan.nair.761@gmail.com','ECE','22STUCHH010761','password',4,8,2022,'BTECH','7000005287'),
(313,'Varun Iyer','varun.iyer.762@gmail.com','ECE','22STUCHH010762','password',4,8,2022,'BTECH','7000005304'),
(314,'Harsha Varma','harsha.varma.763@gmail.com','ECE','22STUCHH010763','password',4,8,2022,'BTECH','7000005321'),
(315,'Karthik Mishra','karthik.mishra.764@gmail.com','ECE','22STUCHH010764','password',4,8,2022,'BTECH','7000005338'),
(316,'Abhinav Pillai','abhinav.pillai.765@gmail.com','ECE','22STUCHH010765','password',4,8,2022,'BTECH','7000005355'),
(317,'Pranav Joshi','pranav.joshi.766@gmail.com','ECE','22STUCHH010766','password',4,8,2022,'BTECH','7000005372'),
(318,'Rahul Goud','rahul.goud.767@gmail.com','ECE','22STUCHH010767','password',4,8,2022,'BTECH','7000005389'),
(319,'Naveen Babu','naveen.babu.768@gmail.com','ECE','22STUCHH010768','password',4,8,2022,'BTECH','7000005406'),
(320,'Manoj Mohan','manoj.mohan.769@gmail.com','ECE','22STUCHH010769','password',4,8,2022,'BTECH','7000005423'),
(321,'Akhil Rani','akhil.rani.770@gmail.com','ECE','22STUCHH010770','password',4,8,2022,'BTECH','7000005440'),
(322,'Tarun Devi','tarun.devi.771@gmail.com','ECE','22STUCHH010771','password',4,8,2022,'BTECH','7000005457'),
(323,'Vivek Sai','vivek.sai.772@gmail.com','ECE','22STUCHH010772','password',4,8,2022,'BTECH','7000005474'),
(324,'Pavan Prasad','pavan.prasad.773@gmail.com','ECE','22STUCHH010773','password',4,8,2022,'BTECH','7000005491'),
(325,'Yash Teja','yash.teja.774@gmail.com','ECE','22STUCHH010774','password',4,8,2022,'BTECH','7000005508'),
(326,'Tejas Kiran','tejas.kiran.775@gmail.com','ECE','22STUCHH010775','password',4,8,2022,'BTECH','7000005525'),
(327,'Ritesh Srinivas','ritesh.srinivas.776@gmail.com','ECE','22STUCHH010776','password',4,8,2022,'BTECH','7000005542'),
(328,'Lokesh Kashyap','lokesh.kashyap.777@gmail.com','ECE','22STUCHH010777','password',4,8,2022,'BTECH','7000005559'),
(329,'Sandeep Reddy','sandeep.reddy.778@gmail.com','ECE','22STUCHH010778','password',4,8,2022,'BTECH','7000005576'),
(330,'Nitin Naik','nitin.naik.779@gmail.com','ECE','22STUCHH010779','password',4,8,2022,'BTECH','7000005593'),
(331,'Ananya Reddy','ananya.reddy.780@gmail.com','ECE','22STUCHH010780','password',4,8,2022,'BTECH','7000005610'),
(332,'Saanvi Sharma','saanvi.sharma.781@gmail.com','ECE','22STUCHH010781','password',4,8,2022,'BTECH','7000005627'),
(333,'Diya Verma','diya.verma.782@gmail.com','ECE','22STUCHH010782','password',4,8,2022,'BTECH','7000005644'),
(334,'Aadhya Gupta','aadhya.gupta.783@gmail.com','ECE','22STUCHH010783','password',4,8,2022,'BTECH','7000005661'),
(335,'Ira Yadav','ira.yadav.784@gmail.com','ECE','22STUCHH010784','password',4,8,2022,'BTECH','7000005678'),
(336,'Myra Rao','myra.rao.785@gmail.com','ECE','22STUCHH010785','password',4,8,2022,'BTECH','7000005695'),
(337,'Kiara Naidu','kiara.naidu.786@gmail.com','ECE','22STUCHH010786','password',4,8,2022,'BTECH','7000005712'),
(338,'Nitya Patel','nitya.patel.787@gmail.com','ECE','22STUCHH010787','password',4,8,2022,'BTECH','7000005729'),
(339,'Ishita Kumar','ishita.kumar.788@gmail.com','ECE','22STUCHH010788','password',4,8,2022,'BTECH','7000005746'),
(340,'Prisha Singh','prisha.singh.789@gmail.com','ECE','22STUCHH010789','password',4,8,2022,'BTECH','7000005763'),
(341,'Meghana Chowdary','meghana.chowdary.790@gmail.com','ECE','22STUCHH010790','password',4,8,2022,'BTECH','7000005780'),
(342,'Harini Nair','harini.nair.791@gmail.com','ECE','22STUCHH010791','password',4,8,2022,'BTECH','7000005797'),
(343,'Sneha Iyer','sneha.iyer.792@gmail.com','ECE','22STUCHH010792','password',4,8,2022,'BTECH','7000005814'),
(344,'Keerthana Varma','keerthana.varma.793@gmail.com','ECE','22STUCHH010793','password',4,8,2022,'BTECH','7000005831'),
(345,'Anvi Mishra','anvi.mishra.794@gmail.com','ECE','22STUCHH010794','password',4,8,2022,'BTECH','7000005848'),
(346,'Ritika Pillai','ritika.pillai.795@gmail.com','ECE','22STUCHH010795','password',4,8,2022,'BTECH','7000005865'),
(347,'Navya Joshi','navya.joshi.796@gmail.com','ECE','22STUCHH010796','password',4,8,2022,'BTECH','7000005882'),
(348,'Deepika Goud','deepika.goud.797@gmail.com','ECE','22STUCHH010797','password',4,8,2022,'BTECH','7000005899'),
(349,'Sravya Babu','sravya.babu.798@gmail.com','ECE','22STUCHH010798','password',4,8,2022,'BTECH','7000005916'),
(350,'Tanvi Mohan','tanvi.mohan.799@gmail.com','ECE','22STUCHH010799','password',4,8,2022,'BTECH','7000005933'),
(351,'Aarav Chowdary','aarav.chowdary.750@gmail.com','CSEAI','22STUCHH010750','password',4,8,2022,'BTECH','7000005950'),
(352,'Vivaan Nair','vivaan.nair.751@gmail.com','CSEAI','22STUCHH010751','password',4,8,2022,'BTECH','7000005967'),
(353,'Aditya Iyer','aditya.iyer.752@gmail.com','CSEAI','22STUCHH010752','password',4,8,2022,'BTECH','7000005984'),
(354,'Vihaan Varma','vihaan.varma.753@gmail.com','CSEAI','22STUCHH010753','password',4,8,2022,'BTECH','7000006001'),
(355,'Arjun Mishra','arjun.mishra.754@gmail.com','CSEAI','22STUCHH010754','password',4,8,2022,'BTECH','7000006018'),
(356,'Sai Pillai','sai.pillai.755@gmail.com','CSEAI','22STUCHH010755','password',4,8,2022,'BTECH','7000006035'),
(357,'Krish Joshi','krish.joshi.756@gmail.com','CSEAI','22STUCHH010756','password',4,8,2022,'BTECH','7000006052'),
(358,'Ishaan Goud','ishaan.goud.757@gmail.com','CSEAI','22STUCHH010757','password',4,8,2022,'BTECH','7000006069'),
(359,'Reyansh Babu','reyansh.babu.758@gmail.com','CSEAI','22STUCHH010758','password',4,8,2022,'BTECH','7000006086'),
(360,'Atharv Mohan','atharv.mohan.759@gmail.com','CSEAI','22STUCHH010759','password',4,8,2022,'BTECH','7000006103'),
(361,'Nihal Rani','nihal.rani.760@gmail.com','CSEAI','22STUCHH010760','password',4,8,2022,'BTECH','7000006120'),
(362,'Rohan Devi','rohan.devi.761@gmail.com','CSEAI','22STUCHH010761','password',4,8,2022,'BTECH','7000006137'),
(363,'Varun Sai','varun.sai.762@gmail.com','CSEAI','22STUCHH010762','password',4,8,2022,'BTECH','7000006154'),
(364,'Harsha Prasad','harsha.prasad.763@gmail.com','CSEAI','22STUCHH010763','password',4,8,2022,'BTECH','7000006171'),
(365,'Karthik Teja','karthik.teja.764@gmail.com','CSEAI','22STUCHH010764','password',4,8,2022,'BTECH','7000006188'),
(366,'Abhinav Kiran','abhinav.kiran.765@gmail.com','CSEAI','22STUCHH010765','password',4,8,2022,'BTECH','7000006205'),
(367,'Pranav Srinivas','pranav.srinivas.766@gmail.com','CSEAI','22STUCHH010766','password',4,8,2022,'BTECH','7000006222'),
(368,'Rahul Kashyap','rahul.kashyap.767@gmail.com','CSEAI','22STUCHH010767','password',4,8,2022,'BTECH','7000006239'),
(369,'Naveen Reddy','naveen.reddy.768@gmail.com','CSEAI','22STUCHH010768','password',4,8,2022,'BTECH','7000006256'),
(370,'Manoj Naik','manoj.naik.769@gmail.com','CSEAI','22STUCHH010769','password',4,8,2022,'BTECH','7000006273'),
(371,'Akhil Reddy','akhil.reddy.770@gmail.com','CSEAI','22STUCHH010770','password',4,8,2022,'BTECH','7000006290'),
(372,'Tarun Sharma','tarun.sharma.771@gmail.com','CSEAI','22STUCHH010771','password',4,8,2022,'BTECH','7000006307'),
(373,'Vivek Verma','vivek.verma.772@gmail.com','CSEAI','22STUCHH010772','password',4,8,2022,'BTECH','7000006324'),
(374,'Pavan Gupta','pavan.gupta.773@gmail.com','CSEAI','22STUCHH010773','password',4,8,2022,'BTECH','7000006341'),
(375,'Yash Yadav','yash.yadav.774@gmail.com','CSEAI','22STUCHH010774','password',4,8,2022,'BTECH','7000006358'),
(376,'Tejas Rao','tejas.rao.775@gmail.com','CSEAI','22STUCHH010775','password',4,8,2022,'BTECH','7000006375'),
(377,'Ritesh Naidu','ritesh.naidu.776@gmail.com','CSEAI','22STUCHH010776','password',4,8,2022,'BTECH','7000006392'),
(378,'Lokesh Patel','lokesh.patel.777@gmail.com','CSEAI','22STUCHH010777','password',4,8,2022,'BTECH','7000006409'),
(379,'Sandeep Kumar','sandeep.kumar.778@gmail.com','CSEAI','22STUCHH010778','password',4,8,2022,'BTECH','7000006426'),
(380,'Nitin Singh','nitin.singh.779@gmail.com','CSEAI','22STUCHH010779','password',4,8,2022,'BTECH','7000006443'),
(381,'Ananya Chowdary','ananya.chowdary.100@gmail.com','BCA','25BCAHH010100','password',1,2,2025,'BCA','7000006460'),
(382,'Saanvi Nair','saanvi.nair.101@gmail.com','BCA','25BCAHH010101','password',1,2,2025,'BCA','7000006477'),
(383,'Diya Iyer','diya.iyer.102@gmail.com','BCA','25BCAHH010102','password',1,2,2025,'BCA','7000006494'),
(384,'Aadhya Varma','aadhya.varma.103@gmail.com','BCA','25BCAHH010103','password',1,2,2025,'BCA','7000006511'),
(385,'Ira Mishra','ira.mishra.104@gmail.com','BCA','25BCAHH010104','password',1,2,2025,'BCA','7000006528'),
(386,'Myra Pillai','myra.pillai.105@gmail.com','BCA','25BCAHH010105','password',1,2,2025,'BCA','7000006545'),
(387,'Kiara Joshi','kiara.joshi.106@gmail.com','BCA','25BCAHH010106','password',1,2,2025,'BCA','7000006562'),
(388,'Nitya Goud','nitya.goud.107@gmail.com','BCA','25BCAHH010107','password',1,2,2025,'BCA','7000006579'),
(389,'Ishita Babu','ishita.babu.108@gmail.com','BCA','25BCAHH010108','password',1,2,2025,'BCA','7000006596'),
(390,'Prisha Mohan','prisha.mohan.109@gmail.com','BCA','25BCAHH010109','password',1,2,2025,'BCA','7000006613'),
(391,'Meghana Rani','meghana.rani.110@gmail.com','BCA','25BCAHH010110','password',1,2,2025,'BCA','7000006630'),
(392,'Harini Devi','harini.devi.111@gmail.com','BCA','25BCAHH010111','password',1,2,2025,'BCA','7000006647'),
(393,'Sneha Sai','sneha.sai.112@gmail.com','BCA','25BCAHH010112','password',1,2,2025,'BCA','7000006664'),
(394,'Keerthana Prasad','keerthana.prasad.113@gmail.com','BCA','25BCAHH010113','password',1,2,2025,'BCA','7000006681'),
(395,'Anvi Teja','anvi.teja.114@gmail.com','BCA','25BCAHH010114','password',1,2,2025,'BCA','7000006698'),
(396,'Ritika Kiran','ritika.kiran.115@gmail.com','BCA','25BCAHH010115','password',1,2,2025,'BCA','7000006715'),
(397,'Navya Srinivas','navya.srinivas.116@gmail.com','BCA','25BCAHH010116','password',1,2,2025,'BCA','7000006732'),
(398,'Deepika Kashyap','deepika.kashyap.117@gmail.com','BCA','25BCAHH010117','password',1,2,2025,'BCA','7000006749'),
(399,'Sravya Reddy','sravya.reddy.118@gmail.com','BCA','25BCAHH010118','password',1,2,2025,'BCA','7000006766'),
(400,'Tanvi Naik','tanvi.naik.119@gmail.com','BCA','25BCAHH010119','password',1,2,2025,'BCA','7000006783'),
(401,'Aarav Reddy','aarav.reddy.120@gmail.com','BCA','25BCAHH010120','password',1,2,2025,'BCA','7000006800'),
(402,'Vivaan Sharma','vivaan.sharma.121@gmail.com','BCA','25BCAHH010121','password',1,2,2025,'BCA','7000006817'),
(403,'Aditya Verma','aditya.verma.122@gmail.com','BCA','25BCAHH010122','password',1,2,2025,'BCA','7000006834'),
(404,'Vihaan Gupta','vihaan.gupta.123@gmail.com','BCA','25BCAHH010123','password',1,2,2025,'BCA','7000006851'),
(405,'Arjun Yadav','arjun.yadav.124@gmail.com','BCA','25BCAHH010124','password',1,2,2025,'BCA','7000006868'),
(406,'Sai Rao','sai.rao.125@gmail.com','BCA','25BCAHH010125','password',1,2,2025,'BCA','7000006885'),
(407,'Krish Naidu','krish.naidu.126@gmail.com','BCA','25BCAHH010126','password',1,2,2025,'BCA','7000006902'),
(408,'Ishaan Patel','ishaan.patel.127@gmail.com','BCA','25BCAHH010127','password',1,2,2025,'BCA','7000006919'),
(409,'Reyansh Kumar','reyansh.kumar.128@gmail.com','BCA','25BCAHH010128','password',1,2,2025,'BCA','7000006936'),
(410,'Atharv Singh','atharv.singh.129@gmail.com','BCA','25BCAHH010129','password',1,2,2025,'BCA','7000006953'),
(411,'Nihal Chowdary','nihal.chowdary.130@gmail.com','BCA','25BCAHH010130','password',1,2,2025,'BCA','7000006970'),
(412,'Rohan Nair','rohan.nair.131@gmail.com','BCA','25BCAHH010131','password',1,2,2025,'BCA','7000006987'),
(413,'Varun Iyer','varun.iyer.132@gmail.com','BCA','25BCAHH010132','password',1,2,2025,'BCA','7000007004'),
(414,'Harsha Varma','harsha.varma.133@gmail.com','BCA','25BCAHH010133','password',1,2,2025,'BCA','7000007021'),
(415,'Karthik Mishra','karthik.mishra.134@gmail.com','BCA','25BCAHH010134','password',1,2,2025,'BCA','7000007038'),
(416,'Abhinav Rani','abhinav.rani.300@gmail.com','BCA','24BCAHH010300','password',2,4,2024,'BCA','7000007055'),
(417,'Pranav Devi','pranav.devi.301@gmail.com','BCA','24BCAHH010301','password',2,4,2024,'BCA','7000007072'),
(418,'Rahul Sai','rahul.sai.302@gmail.com','BCA','24BCAHH010302','password',2,4,2024,'BCA','7000007089'),
(419,'Naveen Prasad','naveen.prasad.303@gmail.com','BCA','24BCAHH010303','password',2,4,2024,'BCA','7000007106'),
(420,'Manoj Teja','manoj.teja.304@gmail.com','BCA','24BCAHH010304','password',2,4,2024,'BCA','7000007123'),
(421,'Akhil Kiran','akhil.kiran.305@gmail.com','BCA','24BCAHH010305','password',2,4,2024,'BCA','7000007140'),
(422,'Tarun Srinivas','tarun.srinivas.306@gmail.com','BCA','24BCAHH010306','password',2,4,2024,'BCA','7000007157'),
(423,'Vivek Kashyap','vivek.kashyap.307@gmail.com','BCA','24BCAHH010307','password',2,4,2024,'BCA','7000007174'),
(424,'Pavan Reddy','pavan.reddy.308@gmail.com','BCA','24BCAHH010308','password',2,4,2024,'BCA','7000007191'),
(425,'Yash Naik','yash.naik.309@gmail.com','BCA','24BCAHH010309','password',2,4,2024,'BCA','7000007208'),
(426,'Tejas Reddy','tejas.reddy.310@gmail.com','BCA','24BCAHH010310','password',2,4,2024,'BCA','7000007225'),
(427,'Ritesh Sharma','ritesh.sharma.311@gmail.com','BCA','24BCAHH010311','password',2,4,2024,'BCA','7000007242'),
(428,'Lokesh Verma','lokesh.verma.312@gmail.com','BCA','24BCAHH010312','password',2,4,2024,'BCA','7000007259'),
(429,'Sandeep Gupta','sandeep.gupta.313@gmail.com','BCA','24BCAHH010313','password',2,4,2024,'BCA','7000007276'),
(430,'Nitin Yadav','nitin.yadav.314@gmail.com','BCA','24BCAHH010314','password',2,4,2024,'BCA','7000007293'),
(431,'Ananya Rao','ananya.rao.315@gmail.com','BCA','24BCAHH010315','password',2,4,2024,'BCA','7000007310'),
(432,'Saanvi Naidu','saanvi.naidu.316@gmail.com','BCA','24BCAHH010316','password',2,4,2024,'BCA','7000007327'),
(433,'Diya Patel','diya.patel.317@gmail.com','BCA','24BCAHH010317','password',2,4,2024,'BCA','7000007344'),
(434,'Aadhya Kumar','aadhya.kumar.318@gmail.com','BCA','24BCAHH010318','password',2,4,2024,'BCA','7000007361'),
(435,'Ira Singh','ira.singh.319@gmail.com','BCA','24BCAHH010319','password',2,4,2024,'BCA','7000007378'),
(436,'Myra Chowdary','myra.chowdary.320@gmail.com','BCA','24BCAHH010320','password',2,4,2024,'BCA','7000007395'),
(437,'Kiara Nair','kiara.nair.321@gmail.com','BCA','24BCAHH010321','password',2,4,2024,'BCA','7000007412'),
(438,'Nitya Iyer','nitya.iyer.322@gmail.com','BCA','24BCAHH010322','password',2,4,2024,'BCA','7000007429'),
(439,'Ishita Varma','ishita.varma.323@gmail.com','BCA','24BCAHH010323','password',2,4,2024,'BCA','7000007446'),
(440,'Prisha Mishra','prisha.mishra.324@gmail.com','BCA','24BCAHH010324','password',2,4,2024,'BCA','7000007463'),
(441,'Meghana Pillai','meghana.pillai.325@gmail.com','BCA','24BCAHH010325','password',2,4,2024,'BCA','7000007480'),
(442,'Harini Joshi','harini.joshi.326@gmail.com','BCA','24BCAHH010326','password',2,4,2024,'BCA','7000007497'),
(443,'Sneha Goud','sneha.goud.327@gmail.com','BCA','24BCAHH010327','password',2,4,2024,'BCA','7000007514'),
(444,'Keerthana Babu','keerthana.babu.328@gmail.com','BCA','24BCAHH010328','password',2,4,2024,'BCA','7000007531'),
(445,'Anvi Mohan','anvi.mohan.329@gmail.com','BCA','24BCAHH010329','password',2,4,2024,'BCA','7000007548'),
(446,'Ritika Rani','ritika.rani.500@gmail.com','BCA','23BCAHH010500','password',3,6,2023,'BCA','7000007565'),
(447,'Navya Devi','navya.devi.501@gmail.com','BCA','23BCAHH010501','password',3,6,2023,'BCA','7000007582'),
(448,'Deepika Sai','deepika.sai.502@gmail.com','BCA','23BCAHH010502','password',3,6,2023,'BCA','7000007599'),
(449,'Sravya Prasad','sravya.prasad.503@gmail.com','BCA','23BCAHH010503','password',3,6,2023,'BCA','7000007616'),
(450,'Tanvi Teja','tanvi.teja.504@gmail.com','BCA','23BCAHH010504','password',3,6,2023,'BCA','7000007633'),
(451,'Aarav Kiran','aarav.kiran.505@gmail.com','BCA','23BCAHH010505','password',3,6,2023,'BCA','7000007650'),
(452,'Vivaan Srinivas','vivaan.srinivas.506@gmail.com','BCA','23BCAHH010506','password',3,6,2023,'BCA','7000007667'),
(453,'Aditya Kashyap','aditya.kashyap.507@gmail.com','BCA','23BCAHH010507','password',3,6,2023,'BCA','7000007684'),
(454,'Vihaan Reddy','vihaan.reddy.508@gmail.com','BCA','23BCAHH010508','password',3,6,2023,'BCA','7000007701'),
(455,'Arjun Naik','arjun.naik.509@gmail.com','BCA','23BCAHH010509','password',3,6,2023,'BCA','7000007718'),
(456,'Sai Reddy','sai.reddy.510@gmail.com','BCA','23BCAHH010510','password',3,6,2023,'BCA','7000007735'),
(457,'Krish Sharma','krish.sharma.511@gmail.com','BCA','23BCAHH010511','password',3,6,2023,'BCA','7000007752'),
(458,'Ishaan Verma','ishaan.verma.512@gmail.com','BCA','23BCAHH010512','password',3,6,2023,'BCA','7000007769'),
(459,'Reyansh Gupta','reyansh.gupta.513@gmail.com','BCA','23BCAHH010513','password',3,6,2023,'BCA','7000007786'),
(460,'Atharv Yadav','atharv.yadav.514@gmail.com','BCA','23BCAHH010514','password',3,6,2023,'BCA','7000007803'),
(461,'Nihal Rao','nihal.rao.515@gmail.com','BCA','23BCAHH010515','password',3,6,2023,'BCA','7000007820'),
(462,'Rohan Naidu','rohan.naidu.516@gmail.com','BCA','23BCAHH010516','password',3,6,2023,'BCA','7000007837'),
(463,'Varun Patel','varun.patel.517@gmail.com','BCA','23BCAHH010517','password',3,6,2023,'BCA','7000007854'),
(464,'Harsha Kumar','harsha.kumar.518@gmail.com','BCA','23BCAHH010518','password',3,6,2023,'BCA','7000007871'),
(465,'Karthik Singh','karthik.singh.519@gmail.com','BCA','23BCAHH010519','password',3,6,2023,'BCA','7000007888'),
(466,'Abhinav Reddy','abhinav.reddy.100@gmail.com','BSC','25BSCHH010100','password',1,2,2025,'BSC','7000007905'),
(467,'Pranav Sharma','pranav.sharma.101@gmail.com','BSC','25BSCHH010101','password',1,2,2025,'BSC','7000007922'),
(468,'Rahul Verma','rahul.verma.102@gmail.com','BSC','25BSCHH010102','password',1,2,2025,'BSC','7000007939'),
(469,'Naveen Gupta','naveen.gupta.103@gmail.com','BSC','25BSCHH010103','password',1,2,2025,'BSC','7000007956'),
(470,'Manoj Yadav','manoj.yadav.104@gmail.com','BSC','25BSCHH010104','password',1,2,2025,'BSC','7000007973'),
(471,'Akhil Rao','akhil.rao.105@gmail.com','BSC','25BSCHH010105','password',1,2,2025,'BSC','7000007990'),
(472,'Tarun Naidu','tarun.naidu.106@gmail.com','BSC','25BSCHH010106','password',1,2,2025,'BSC','7000008007'),
(473,'Vivek Patel','vivek.patel.107@gmail.com','BSC','25BSCHH010107','password',1,2,2025,'BSC','7000008024'),
(474,'Pavan Kumar','pavan.kumar.108@gmail.com','BSC','25BSCHH010108','password',1,2,2025,'BSC','7000008041'),
(475,'Yash Singh','yash.singh.109@gmail.com','BSC','25BSCHH010109','password',1,2,2025,'BSC','7000008058'),
(476,'Tejas Chowdary','tejas.chowdary.110@gmail.com','BSC','25BSCHH010110','password',1,2,2025,'BSC','7000008075'),
(477,'Ritesh Nair','ritesh.nair.111@gmail.com','BSC','25BSCHH010111','password',1,2,2025,'BSC','7000008092'),
(478,'Lokesh Iyer','lokesh.iyer.112@gmail.com','BSC','25BSCHH010112','password',1,2,2025,'BSC','7000008109'),
(479,'Sandeep Varma','sandeep.varma.113@gmail.com','BSC','25BSCHH010113','password',1,2,2025,'BSC','7000008126'),
(480,'Nitin Mishra','nitin.mishra.114@gmail.com','BSC','25BSCHH010114','password',1,2,2025,'BSC','7000008143'),
(481,'Ananya Reddy','ananya.reddy.300@gmail.com','BSC','24BSCHH010300','password',2,4,2024,'BSC','7000008160'),
(482,'Saanvi Sharma','saanvi.sharma.301@gmail.com','BSC','24BSCHH010301','password',2,4,2024,'BSC','7000008177'),
(483,'Diya Verma','diya.verma.302@gmail.com','BSC','24BSCHH010302','password',2,4,2024,'BSC','7000008194'),
(484,'Aadhya Gupta','aadhya.gupta.303@gmail.com','BSC','24BSCHH010303','password',2,4,2024,'BSC','7000008211'),
(485,'Ira Yadav','ira.yadav.304@gmail.com','BSC','24BSCHH010304','password',2,4,2024,'BSC','7000008228'),
(486,'Myra Rao','myra.rao.305@gmail.com','BSC','24BSCHH010305','password',2,4,2024,'BSC','7000008245'),
(487,'Kiara Naidu','kiara.naidu.306@gmail.com','BSC','24BSCHH010306','password',2,4,2024,'BSC','7000008262'),
(488,'Nitya Patel','nitya.patel.307@gmail.com','BSC','24BSCHH010307','password',2,4,2024,'BSC','7000008279'),
(489,'Ishita Kumar','ishita.kumar.308@gmail.com','BSC','24BSCHH010308','password',2,4,2024,'BSC','7000008296'),
(490,'Prisha Singh','prisha.singh.309@gmail.com','BSC','24BSCHH010309','password',2,4,2024,'BSC','7000008313'),
(491,'Meghana Rani','meghana.rani.500@gmail.com','BSC','23BSCHH010500','password',3,6,2023,'BSC','7000008330'),
(492,'Harini Devi','harini.devi.501@gmail.com','BSC','23BSCHH010501','password',3,6,2023,'BSC','7000008347'),
(493,'Sneha Sai','sneha.sai.502@gmail.com','BSC','23BSCHH010502','password',3,6,2023,'BSC','7000008364'),
(494,'Keerthana Prasad','keerthana.prasad.503@gmail.com','BSC','23BSCHH010503','password',3,6,2023,'BSC','7000008381'),
(495,'Anvi Teja','anvi.teja.504@gmail.com','BSC','23BSCHH010504','password',3,6,2023,'BSC','7000008398'),
(496,'Ritika Kiran','ritika.kiran.505@gmail.com','BSC','23BSCHH010505','password',3,6,2023,'BSC','7000008415'),
(497,'Navya Srinivas','navya.srinivas.506@gmail.com','BSC','23BSCHH010506','password',3,6,2023,'BSC','7000008432'),
(498,'Deepika Kashyap','deepika.kashyap.507@gmail.com','BSC','23BSCHH010507','password',3,6,2023,'BSC','7000008449'),
(499,'Sravya Reddy','sravya.reddy.508@gmail.com','BSC','23BSCHH010508','password',3,6,2023,'BSC','7000008466'),
(500,'Tanvi Naik','tanvi.naik.509@gmail.com','BSC','23BSCHH010509','password',3,6,2023,'BSC','7000008483');
/*!40000 ALTER TABLE `students` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `faculty_chat_messages`
--

DROP TABLE IF EXISTS `faculty_chat_messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `faculty_chat_messages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `student_id` int NOT NULL,
  `faculty_id` int NOT NULL,
  `sender_role` varchar(20) NOT NULL,
  `message` text NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `student_id` (`student_id`),
  KEY `faculty_id` (`faculty_id`),
  CONSTRAINT `faculty_chat_messages_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`) ON DELETE CASCADE,
  CONSTRAINT `faculty_chat_messages_ibfk_2` FOREIGN KEY (`faculty_id`) REFERENCES `admin` (`admin_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `faculty_chat_messages`
--

LOCK TABLES `faculty_chat_messages` WRITE;
/*!40000 ALTER TABLE `faculty_chat_messages` DISABLE KEYS */;
/*!40000 ALTER TABLE `faculty_chat_messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `faculty_meeting_requests`
--

DROP TABLE IF EXISTS `faculty_meeting_requests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `faculty_meeting_requests` (
  `id` int NOT NULL AUTO_INCREMENT,
  `student_id` int NOT NULL,
  `faculty_id` int NOT NULL,
  `request_message` text NOT NULL,
  `preferred_slot` varchar(120) DEFAULT NULL,
  `status` varchar(20) DEFAULT 'Pending',
  `faculty_response` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `student_id` (`student_id`),
  KEY `faculty_id` (`faculty_id`),
  CONSTRAINT `faculty_meeting_requests_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`) ON DELETE CASCADE,
  CONSTRAINT `faculty_meeting_requests_ibfk_2` FOREIGN KEY (`faculty_id`) REFERENCES `admin` (`admin_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `faculty_meeting_requests`
--

LOCK TABLES `faculty_meeting_requests` WRITE;
/*!40000 ALTER TABLE `faculty_meeting_requests` DISABLE KEYS */;
/*!40000 ALTER TABLE `faculty_meeting_requests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `faculty_schedule`
--

DROP TABLE IF EXISTS `faculty_schedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `faculty_schedule` (
  `id` int NOT NULL AUTO_INCREMENT,
  `faculty_id` int NOT NULL,
  `title` varchar(120) NOT NULL,
  `day_name` varchar(20) NOT NULL,
  `start_time` varchar(20) NOT NULL,
  `end_time` varchar(20) NOT NULL,
  `location` varchar(120) DEFAULT NULL,
  `availability_note` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `faculty_id` (`faculty_id`),
  CONSTRAINT `faculty_schedule_ibfk_1` FOREIGN KEY (`faculty_id`) REFERENCES `admin` (`admin_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `faculty_schedule`
--

LOCK TABLES `faculty_schedule` WRITE;
/*!40000 ALTER TABLE `faculty_schedule` DISABLE KEYS */;
/*!40000 ALTER TABLE `faculty_schedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `classrooms`
--

DROP TABLE IF EXISTS `classrooms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `classrooms` (
  `id` int NOT NULL AUTO_INCREMENT,
  `room_number` varchar(50) NOT NULL,
  `block_name` varchar(100) DEFAULT NULL,
  `total_seats` int NOT NULL,
  `columns_count` int DEFAULT '6',
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `classrooms`
--

LOCK TABLES `classrooms` WRITE;
/*!40000 ALTER TABLE `classrooms` DISABLE KEYS */;
/*!40000 ALTER TABLE `classrooms` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exam_seating_plans`
--

DROP TABLE IF EXISTS `exam_seating_plans`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `exam_seating_plans` (
  `id` int NOT NULL AUTO_INCREMENT,
  `exam_name` varchar(150) NOT NULL,
  `subject_name` varchar(150) NOT NULL,
  `exam_date` date NOT NULL,
  `exam_time` varchar(50) NOT NULL,
  `exam_end_time` varchar(50) DEFAULT NULL,
  `strategy` varchar(50) NOT NULL,
  `room_reveal_hours_before` int DEFAULT '12',
  `seat_reveal_minutes_before` int DEFAULT '10',
  `selected_groups_json` longtext,
  `room_ids_json` longtext,
  `created_by` int DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `created_by` (`created_by`),
  CONSTRAINT `exam_seating_plans_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `admin` (`admin_id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exam_seating_plans`
--

LOCK TABLES `exam_seating_plans` WRITE;
/*!40000 ALTER TABLE `exam_seating_plans` DISABLE KEYS */;
/*!40000 ALTER TABLE `exam_seating_plans` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exam_seating_allocations`
--

DROP TABLE IF EXISTS `exam_seating_allocations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `exam_seating_allocations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `plan_id` int NOT NULL,
  `student_id` int NOT NULL,
  `classroom_id` int NOT NULL,
  `subject_name` varchar(150) NOT NULL,
  `room_number` varchar(50) NOT NULL,
  `seat_number` int NOT NULL,
  `seat_label` varchar(20) NOT NULL,
  `seat_row` int NOT NULL,
  `seat_column` int NOT NULL,
  `group_label` varchar(100) NOT NULL,
  `ordering_value` varchar(120) DEFAULT NULL,
  `room_visible_at` datetime NOT NULL,
  `seat_visible_at` datetime NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `plan_id` (`plan_id`),
  KEY `student_id` (`student_id`),
  KEY `classroom_id` (`classroom_id`),
  CONSTRAINT `exam_seating_allocations_ibfk_1` FOREIGN KEY (`plan_id`) REFERENCES `exam_seating_plans` (`id`) ON DELETE CASCADE,
  CONSTRAINT `exam_seating_allocations_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`) ON DELETE CASCADE,
  CONSTRAINT `exam_seating_allocations_ibfk_3` FOREIGN KEY (`classroom_id`) REFERENCES `classrooms` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exam_seating_allocations`
--

LOCK TABLES `exam_seating_allocations` WRITE;
/*!40000 ALTER TABLE `exam_seating_allocations` DISABLE KEYS */;
/*!40000 ALTER TABLE `exam_seating_allocations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subjects`
--

DROP TABLE IF EXISTS `subjects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `subjects` (
  `id` int NOT NULL AUTO_INCREMENT,
  `branch` varchar(50) DEFAULT NULL,
  `year` int DEFAULT NULL,
  `semester` int DEFAULT NULL,
  `subject_name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=180 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subjects`
--

LOCK TABLES `subjects` WRITE;
/*!40000 ALTER TABLE `subjects` DISABLE KEYS */;
INSERT INTO `subjects` VALUES (1,'ALL',1,1,'Mathematics I'),(2,'ALL',1,1,'Physics'),(3,'ALL',1,1,'Programming in C'),(4,'ALL',1,1,'Engineering Graphics'),(5,'ALL',1,1,'Basic Electrical Engineering'),(6,'ALL',1,1,'English Communication'),(7,'ALL',1,2,'Mathematics II'),(8,'ALL',1,2,'Chemistry'),(9,'ALL',1,2,'Data Structures (Intro)'),(10,'ALL',1,2,'Digital Logic Design'),(11,'ALL',1,2,'Environmental Science'),(12,'ALL',1,2,'Workshop / Lab'),(13,'CSE',2,3,'OOP using Java'),(14,'CSE',2,3,'Data Structures & Algorithms'),(15,'CSE',2,3,'Database Management Systems'),(16,'CSE',2,3,'Computer Organization'),(17,'CSE',2,3,'Discrete Mathematics'),(18,'CSE',2,4,'Operating Systems'),(19,'CSE',2,4,'Design & Analysis of Algorithms'),(20,'CSE',2,4,'Software Engineering'),(21,'CSE',2,4,'Computer Networks'),(22,'CSE',2,4,'Web Technologies'),(23,'CSE',3,5,'Compiler Design'),(24,'CSE',3,5,'Artificial Intelligence'),(25,'CSE',3,5,'Distributed Systems'),(26,'CSE',3,5,'Mobile Computing'),(27,'CSE',3,5,'Open Elective'),(28,'CSE',3,6,'Machine Learning'),(29,'CSE',3,6,'Cloud Computing'),(30,'CSE',3,6,'Cyber Security'),(31,'CSE',3,6,'Big Data Analytics'),(32,'CSE',3,6,'Professional Elective'),(33,'CSE',4,7,'Advanced Machine Learning'),(34,'CSE',4,7,'Blockchain Technology'),(35,'CSE',4,7,'DevOps'),(36,'CSE',4,7,'Project Phase 1'),(37,'CSE',4,7,'Elective'),(38,'CSE',4,8,'Project Phase 2'),(39,'CSE',4,8,'Internship'),(40,'CSE',4,8,'Seminar'),(41,'CSE',4,8,'Elective'),(42,'CSEAI',2,3,'Python Programming'),(43,'CSEAI',2,3,'Data Structures'),(44,'CSEAI',2,3,'Linear Algebra'),(45,'CSEAI',2,3,'Probability & Statistics'),(46,'CSEAI',2,3,'DBMS'),(47,'CSEAI',2,4,'Advanced Python'),(48,'CSEAI',2,4,'Algorithms'),(49,'CSEAI',2,4,'Operating Systems'),(50,'CSEAI',2,4,'Data Visualization'),(51,'CSEAI',2,4,'Optimization Techniques'),(52,'CSEAI',3,5,'Machine Learning'),(53,'CSEAI',3,5,'Deep Learning'),(54,'CSEAI',3,5,'Natural Language Processing'),(55,'CSEAI',3,5,'Computer Vision'),(56,'CSEAI',3,5,'AI Ethics'),(57,'CSEAI',3,6,'Reinforcement Learning'),(58,'CSEAI',3,6,'Robotics'),(59,'CSEAI',3,6,'Big Data Analytics'),(60,'CSEAI',3,6,'Cloud Computing'),(61,'CSEAI',3,6,'Elective'),(62,'CSEAI',4,7,'Advanced Deep Learning'),(63,'CSEAI',4,7,'AI in Healthcare'),(64,'CSEAI',4,7,'Edge AI'),(65,'CSEAI',4,7,'Project Phase 1'),(66,'CSEAI',4,7,'Elective'),(67,'CSEAI',4,8,'Project Phase 2'),(68,'CSEAI',4,8,'Internship'),(69,'CSEAI',4,8,'Seminar'),(70,'CSEDS',2,3,'Python'),(71,'CSEDS',2,3,'Statistics'),(72,'CSEDS',2,3,'Data Structures'),(73,'CSEDS',2,3,'DBMS'),(74,'CSEDS',2,3,'Linear Algebra'),(75,'CSEDS',2,4,'Advanced Statistics'),(76,'CSEDS',2,4,'Algorithms'),(77,'CSEDS',2,4,'Operating Systems'),(78,'CSEDS',2,4,'Data Visualization'),(79,'CSEDS',2,4,'Data Warehousing'),(80,'CSEDS',3,5,'Data Mining'),(81,'CSEDS',3,5,'Machine Learning'),(82,'CSEDS',3,5,'Big Data Technologies'),(83,'CSEDS',3,5,'Cloud Computing'),(84,'CSEDS',3,5,'Elective'),(85,'CSEDS',3,6,'Deep Learning'),(86,'CSEDS',3,6,'Predictive Analytics'),(87,'CSEDS',3,6,'NLP'),(88,'CSEDS',3,6,'Data Engineering'),(89,'CSEDS',3,6,'Elective'),(90,'CSEDS',4,7,'Advanced Analytics'),(91,'CSEDS',4,7,'MLOps'),(92,'CSEDS',4,7,'AI Applications'),(93,'CSEDS',4,7,'Project Phase 1'),(94,'CSEDS',4,8,'Project Phase 2'),(95,'CSEDS',4,8,'Internship'),(96,'CSEDS',4,8,'Seminar'),(97,'ECE',2,3,'Electronic Devices'),(98,'ECE',2,3,'Network Theory'),(99,'ECE',2,3,'Signals & Systems'),(100,'ECE',2,3,'Analog Circuits'),(101,'ECE',2,3,'Digital Electronics'),(102,'ECE',2,4,'Microprocessors'),(103,'ECE',2,4,'Control Systems'),(104,'ECE',2,4,'Analog Communication'),(105,'ECE',2,4,'Electromagnetic Theory'),(106,'ECE',2,4,'Linear IC Applications'),(107,'ECE',3,5,'Digital Communication'),(108,'ECE',3,5,'VLSI Design'),(109,'ECE',3,5,'Embedded Systems'),(110,'ECE',3,5,'DSP'),(111,'ECE',3,5,'Elective'),(112,'ECE',3,6,'Wireless Communication'),(113,'ECE',3,6,'IoT'),(114,'ECE',3,6,'Optical Communication'),(115,'ECE',3,6,'Radar Systems'),(116,'ECE',3,6,'Elective'),(117,'ECE',4,7,'Advanced Communication Systems'),(118,'ECE',4,7,'Satellite Communication'),(119,'ECE',4,7,'5G Technology'),(120,'ECE',4,7,'Project Phase 1'),(121,'ECE',4,8,'Project Phase 2'),(122,'ECE',4,8,'Internship'),(123,'ECE',4,8,'Seminar'),(124,'BCA',1,1,'Fundamentals of Computers'),(125,'BCA',1,1,'Programming in C'),(126,'BCA',1,1,'Mathematics'),(127,'BCA',1,1,'English'),(128,'BCA',1,1,'Digital Fundamentals'),(129,'BCA',1,2,'Data Structures'),(130,'BCA',1,2,'OOP using C++'),(131,'BCA',1,2,'DBMS'),(132,'BCA',1,2,'Web Development'),(133,'BCA',1,2,'Environmental Studies'),(134,'BCA',2,3,'Java Programming'),(135,'BCA',2,3,'Operating Systems'),(136,'BCA',2,3,'Computer Networks'),(137,'BCA',2,3,'Software Engineering'),(138,'BCA',2,3,'Mathematics II'),(139,'BCA',2,4,'Python Programming'),(140,'BCA',2,4,'Web Technologies'),(141,'BCA',2,4,'Cloud Computing'),(142,'BCA',2,4,'Mobile App Development'),(143,'BCA',2,4,'Elective'),(144,'BCA',3,5,'Artificial Intelligence'),(145,'BCA',3,5,'Data Analytics'),(146,'BCA',3,5,'Cyber Security'),(147,'BCA',3,5,'IoT'),(148,'BCA',3,5,'Project Phase 1'),(149,'BCA',3,6,'Project Phase 2'),(150,'BCA',3,6,'Internship'),(151,'BCA',3,6,'Seminar'),(152,'BSC',1,1,'Mathematics'),(153,'BSC',1,1,'Computer Fundamentals'),(154,'BSC',1,1,'Programming in C'),(155,'BSC',1,1,'English'),(156,'BSC',1,1,'Physics'),(157,'BSC',1,2,'Data Structures'),(158,'BSC',1,2,'DBMS'),(159,'BSC',1,2,'Java'),(160,'BSC',1,2,'Environmental Science'),(161,'BSC',1,2,'Statistics'),(162,'BSC',2,3,'Operating Systems'),(163,'BSC',2,3,'Computer Networks'),(164,'BSC',2,3,'Software Engineering'),(165,'BSC',2,3,'Mathematics II'),(166,'BSC',2,3,'Elective'),(167,'BSC',2,4,'Data Analytics'),(168,'BSC',2,4,'Machine Learning'),(169,'BSC',2,4,'Artificial Intelligence'),(170,'BSC',2,4,'Big Data'),(171,'BSC',2,4,'Elective'),(172,'BSC',3,5,'Advanced ML'),(173,'BSC',3,5,'Data Visualization'),(174,'BSC',3,5,'Cloud Computing'),(175,'BSC',3,5,'Research Methods'),(176,'BSC',3,5,'Project Phase 1'),(177,'BSC',3,6,'Project Phase 2'),(178,'BSC',3,6,'Internship'),(179,'BSC',3,6,'Seminar');
/*!40000 ALTER TABLE `subjects` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-01  1:32:57
