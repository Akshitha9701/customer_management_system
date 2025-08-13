-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: customer_management
-- ------------------------------------------------------
-- Server version	8.0.40

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
-- Table structure for table `complaints`
--

DROP TABLE IF EXISTS `complaints`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `complaints` (
  `complaint_id` varchar(255) NOT NULL,
  `customer_id` varchar(255) DEFAULT NULL,
  `order_id` varchar(255) DEFAULT NULL,
  `product_name` varchar(255) DEFAULT NULL,
  `complaint` text,
  `complaint_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`complaint_id`),
  KEY `customer_id` (`customer_id`),
  KEY `order_id` (`order_id`),
  CONSTRAINT `complaints_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`),
  CONSTRAINT `complaints_ibfk_2` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `complaints`
--

LOCK TABLES `complaints` WRITE;
/*!40000 ALTER TABLE `complaints` DISABLE KEYS */;
INSERT INTO `complaints` VALUES ('CMP001','CUST001','ORD002','Mouse','stopped working after few days only','2025-03-20 17:13:19'),('CMP002','CUST004','ORD005','Mouse','Mouse is not working properly please look into the matter','2025-03-20 17:15:01'),('CMP003','CUST012','ORD015','Wireless Keyboard','not connecting properly to the pc','2025-04-05 18:30:00');
/*!40000 ALTER TABLE `complaints` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customers` (
  `customer_id` varchar(255) NOT NULL,
  `customer_name` varchar(255) DEFAULT NULL,
  `gender` varchar(255) DEFAULT NULL,
  `email_id` varchar(255) DEFAULT NULL,
  `phone_number` varchar(255) DEFAULT NULL,
  `customer_segment` enum('Individual','Business','Enterprise') DEFAULT 'Individual',
  `status` enum('Active','Inactive') DEFAULT 'Active',
  `total_orders` int DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `last_order_date` date DEFAULT NULL,
  PRIMARY KEY (`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers`
--

LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
INSERT INTO `customers` VALUES ('CUST001','Akshitha','Female','aks123@gmail.com','9364322892','Individual','Inactive',4,'2025-03-20 06:51:29','2025-05-15'),('CUST002','Manasa','Female','manas98@gmail.com','8979725378','Individual','Active',1,'2025-03-20 06:53:14','2025-03-20'),('CUST003','Srilekha','Female','srili200529@gmail.com','8979872378','Individual','Active',2,'2025-03-20 06:53:58','2025-03-20'),('CUST004','Agnesh','Male','agni12@gmail.com','8239872378','Individual','Active',1,'2025-03-20 09:43:39','2025-03-20'),('CUST005','SmartBiz Systems','None','smartbizsystems19@gmail.com','9729147289','Business','Active',1,'2025-03-21 09:50:16','2025-03-21'),('CUST006','TechTrend Innovations','None','techtrendinn436@gmail.com','8467318376','Business','Active',1,'2025-03-21 10:04:00','2025-03-21'),('CUST007','BlueSky Solutions','None','blueskysolutions@gmail.com','8926482744','Business','Active',1,'2025-04-02 07:30:46','2025-04-02'),('CUST008','BrightPath Consulting','None','brightpathcon73@gmail.com','8982748277','Business','Active',1,'2025-04-02 07:31:56','2025-04-02'),('CUST009','Chandrashekar','Male','chadu12@gmail.com','9384759282','Individual','Active',1,'2025-04-04 05:53:29','2025-04-04'),('CUST010','SwiftNest Logistics','None','swiftnestlogs723@gmail.com','7853471829','Business','Active',1,'2025-04-04 06:01:21','2025-04-04'),('CUST011','Urbanflow Traders','None','urbanflowtraders243@gmail.com','9834752874','Business','Active',1,'2025-04-04 06:28:30','2025-04-04'),('CUST012','Silverpeak Systems','None','silverpeaksystems321@gmail.com','8238752874','Business','Active',1,'2025-04-04 06:29:23','2025-04-04'),('CUST013','CoreWave Innovations','None','corewaves7722@gmail.com','8272752872','Business','Active',1,'2025-04-04 06:30:14','2025-04-04'),('CUST014','TitanForge Industries',NULL,'titanforgeind@gmail.com','9384578428','Enterprise','Active',1,'2025-04-04 09:33:30','2025-04-04'),('CUST015','TurboLap Gaming',NULL,'turbogames@gmail.com','9384752292','Business','Active',2,'2025-04-04 10:24:00','2025-07-02'),('CUST016','CompuSphere Enterprises',NULL,'compusphere.ent@gmail.com','041-4617817381','Enterprise','Active',3,'2025-04-04 10:30:25','2025-05-23'),('CUST017','sathyatech pro ',NULL,'sathyatechpro@gmail.com','7489179814','Business','Active',1,'2025-04-07 08:07:49','2025-04-07');
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feedback`
--

DROP TABLE IF EXISTS `feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feedback` (
  `feedback_id` int NOT NULL AUTO_INCREMENT,
  `customer_id` varchar(20) DEFAULT NULL,
  `order_id` varchar(20) DEFAULT NULL,
  `product_name` varchar(255) DEFAULT NULL,
  `rating` int DEFAULT NULL,
  `comment` text,
  `feedback_date` date DEFAULT NULL,
  PRIMARY KEY (`feedback_id`)
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
-- Table structure for table `loyalty_points`
--

DROP TABLE IF EXISTS `loyalty_points`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `loyalty_points` (
  `customer_id` varchar(10) NOT NULL,
  `points` int DEFAULT '0',
  PRIMARY KEY (`customer_id`),
  CONSTRAINT `loyalty_points_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `loyalty_points`
--

LOCK TABLES `loyalty_points` WRITE;
/*!40000 ALTER TABLE `loyalty_points` DISABLE KEYS */;
/*!40000 ALTER TABLE `loyalty_points` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `order_id` varchar(255) NOT NULL,
  `customer_id` varchar(255) DEFAULT NULL,
  `product_name` varchar(255) DEFAULT NULL,
  `order_amount` varchar(255) DEFAULT NULL,
  `quantity` int DEFAULT '1',
  `order_date` date DEFAULT NULL,
  `delivery_status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`order_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES ('ORD001','CUST001','laptop','50000.00',1,'2025-03-20','Delivered'),('ORD002','CUST001','Mouse','2000.00',1,'2025-03-20','Delivered'),('ORD003','CUST003','server','22000.00',1,'2025-03-20','Delivered'),('ORD004','CUST003','Mouse','2000.00',1,'2025-03-20','Delivered'),('ORD005','CUST004','Mouse','2000.00',1,'2025-03-20','Delivered'),('ORD006','CUST008','computers','60000.0',4,'2025-04-02','Delivered'),('ORD007','CUST010','Ultra USB Drive','750.0',3,'2025-04-04','Delivered'),('ORD008','CUST009','Dual Mode Rechargeable Mose','800.0',2,'2025-04-04','Delivered'),('ORD009','CUST002','Advanced Wireless Trackball Mouse','6000.0',1,'2025-04-04','Delivered'),('ORD010','CUST005','Laptop Cooling Pad','500.0',10,'2025-04-04','Delivered'),('ORD011','CUST006','Wireless Keyboard and Mouse Combo','1100.0',3,'2025-04-04','Delivered'),('ORD012','CUST007','Gen9 Tower Server','50000.0',1,'2025-04-04','Delivered'),('ORD013','CUST014','Power Edge T550 Tower server','350000.0',2,'2025-04-04','Delivered'),('ORD014','CUST011','Laptop 13th Gen Core i5','55200.0',2,'2025-04-04','Delivered'),('ORD015','CUST012','Wireless Keyboard with touchpad','1199.0',2,'2025-04-04','Delivered'),('ORD016','CUST013','Mini Voltage Stabiliser','2199.0',2,'2025-04-04','Delivered'),('ORD017','CUST015','ALG 13th Gen Gaming Laptop','62000.0',3,'2025-04-04','Delivered'),('ORD018','CUST016','Laptop 13th Gen Core i5','55199.96',2,'2025-04-04','Delivered'),('ORD019','CUST016','Wireless Keyboard with touchpad','55200.0',3,'2025-04-04','Delivered'),('ORD020','CUST016','Gen 9 Tower Server','50000.0',3,'2025-04-04','Delivered'),('ORD021','CUST001','Dual Mode Rechargeable Mouse','800.0',5,'2025-04-06','Delivered'),('ORD022','CUST001','Laptop Cooling Pad','500.00',3,'2025-04-07','Delivered'),('ORD023','CUST017','Mini Voltage Stabiliser','2199.00',2,'2025-04-07','Delivered'),('ORD024','CUST015','Laptop Cooling Pad','500.00',10,'2025-07-02',NULL);
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `update_total_orders` AFTER INSERT ON `orders` FOR EACH ROW UPDATE customers SET total_orders = total_orders + 1 WHERE customer_id = NEW.customer_id */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `product_id` varchar(20) NOT NULL,
  `product_name` varchar(150) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  PRIMARY KEY (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES ('PROD001','Ultra USB Drive',750.00),('PROD002','Dual Mode Rechargeable Mose',800.00),('PROD003','Advanced Wireless Trackball Mouse',6000.00),('PROD004','Laptop Cooling Pad',500.00),('PROD005','Wireless Keyboard and Mouse Combo',1100.00),('PROD006','Gen9 Tower Server',50000.00),('PROD007','Power Edge T550 Tower server',350000.00),('PROD008','Laptop 13th Gen Core i5',55200.00),('PROD009','Wireless Keyboard with touchpad',1199.00),('PROD010','Mini Voltage Stabiliser',2199.00),('PROD011','ALG 13th Gen Gaming Laptop',62000.00);
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `returns`
--

DROP TABLE IF EXISTS `returns`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `returns` (
  `return_id` varchar(255) NOT NULL,
  `customer_id` varchar(255) DEFAULT NULL,
  `product_name` varchar(255) DEFAULT NULL,
  `reason` text,
  `return_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `order_id` varchar(255) DEFAULT NULL,
  `return_quantity` int DEFAULT NULL,
  PRIMARY KEY (`return_id`),
  KEY `customer_id` (`customer_id`),
  KEY `order_id` (`order_id`),
  CONSTRAINT `returns_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`),
  CONSTRAINT `returns_ibfk_2` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `returns`
--

LOCK TABLES `returns` WRITE;
/*!40000 ALTER TABLE `returns` DISABLE KEYS */;
INSERT INTO `returns` VALUES ('RET001','CUST001','Mouse','Defective','2025-03-20 17:23:58','ORD002',1),('RET002','CUST013','Mini voltage stabiliser','no surge protection','2025-04-05 18:30:00','ORD016',2),('RET003','CUST017','Mini voltage stabiliser','over heating, no surge protection','2025-04-06 18:30:00','ORD023',2);
/*!40000 ALTER TABLE `returns` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `username` varchar(100) NOT NULL,
  `password` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('Akshithakom','aksnetha@123');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-02 12:32:39
