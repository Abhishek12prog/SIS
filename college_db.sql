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
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `year` int DEFAULT NULL,
  `semester` int DEFAULT NULL,
  `joining_year` int DEFAULT NULL,
  `course_type` varchar(20) DEFAULT NULL,
  `phone` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`student_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students`
--

LOCK TABLES `students` WRITE;
/*!40000 ALTER TABLE `students` DISABLE KEYS */;
INSERT INTO `students` VALUES (1,'Rahul','rahul@gmail.com','CSE','rahul','rahul123',2,3,NULL,NULL,NULL),(2,'abhi','abhi@g.com','cse','abhi','12345',1,NULL,NULL,NULL,NULL),(3,'praneeth','praneeth@ifheindia.org','CSEAI','23STUCHH010841','password',NULL,NULL,2023,'BTECH',NULL),(4,'nagraj','nagraj@gmai.com','ECE','23STUCH011382','password',2023,6,2023,'BTECH','9988998876');
/*!40000 ALTER TABLE `students` ENABLE KEYS */;
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
