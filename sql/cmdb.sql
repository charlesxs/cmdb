-- MySQL dump 10.13  Distrib 5.7.17, for osx10.12 (x86_64)
--
-- Host: localhost    Database: cmdb
-- ------------------------------------------------------
-- Server version	5.7.17

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_0e939a4f` (`group_id`),
  KEY `auth_group_permissions_8373b171` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_01ab375a_uniq` (`content_type_id`,`codename`),
  KEY `auth_permission_417f1b1c` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=55 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add group',2,'add_group'),(5,'Can change group',2,'change_group'),(6,'Can delete group',2,'delete_group'),(7,'Can add user',3,'add_user'),(8,'Can change user',3,'change_user'),(9,'Can delete user',3,'delete_user'),(10,'Can add permission',4,'add_permission'),(11,'Can change permission',4,'change_permission'),(12,'Can delete permission',4,'delete_permission'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add idc',7,'add_idc'),(20,'Can change idc',7,'change_idc'),(21,'Can delete idc',7,'delete_idc'),(22,'Can add business line',8,'add_businessline'),(23,'Can change business line',8,'change_businessline'),(24,'Can delete business line',8,'delete_businessline'),(25,'Can add user',9,'add_user'),(26,'Can change user',9,'change_user'),(27,'Can delete user',9,'delete_user'),(28,'Can add asset',10,'add_asset'),(29,'Can change asset',10,'change_asset'),(30,'Can delete asset',10,'delete_asset'),(31,'Can add server',11,'add_server'),(32,'Can change server',11,'change_server'),(33,'Can delete server',11,'delete_server'),(34,'Can add network device',12,'add_networkdevice'),(35,'Can change network device',12,'change_networkdevice'),(36,'Can delete network device',12,'delete_networkdevice'),(37,'Can add network interface',13,'add_networkinterface'),(38,'Can change network interface',13,'change_networkinterface'),(39,'Can delete network interface',13,'delete_networkinterface'),(40,'Can add memory',14,'add_memory'),(41,'Can change memory',14,'change_memory'),(42,'Can delete memory',14,'delete_memory'),(43,'Can add cpu',15,'add_cpu'),(44,'Can change cpu',15,'change_cpu'),(45,'Can delete cpu',15,'delete_cpu'),(46,'Can add disk',16,'add_disk'),(47,'Can change disk',16,'change_disk'),(48,'Can delete disk',16,'delete_disk'),(49,'Can add hw system',17,'add_hwsystem'),(50,'Can change hw system',17,'change_hwsystem'),(51,'Can delete hw system',17,'delete_hwsystem'),(52,'Can add history',18,'add_history'),(53,'Can change history',18,'change_history'),(54,'Can delete history',18,'delete_history');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_e8701ad4` (`user_id`),
  KEY `auth_user_groups_0e939a4f` (`group_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_e8701ad4` (`user_id`),
  KEY `auth_user_user_permissions_8373b171` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cmdb_asset`
--

DROP TABLE IF EXISTS `cmdb_asset`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cmdb_asset` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `serialnum` varchar(100) NOT NULL,
  `asset_type` varchar(120) NOT NULL,
  `cabinet_number` int(11) DEFAULT NULL,
  `cabinet_position` int(11) DEFAULT NULL,
  `create_time` datetime NOT NULL,
  `update_time` datetime NOT NULL,
  `use` varchar(120) NOT NULL,
  `state` smallint(6) NOT NULL,
  `comment` varchar(200) DEFAULT NULL,
  `contact_id` int(11) NOT NULL,
  `idc_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `serialnum` (`serialnum`),
  KEY `cmdb_asset_9ed39e2e` (`state`),
  KEY `cmdb_asset_6d82f13d` (`contact_id`),
  KEY `cmdb_asset_0869e37a` (`idc_id`)
) ENGINE=MyISAM AUTO_INCREMENT=74 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cmdb_asset`
--

LOCK TABLES `cmdb_asset` WRITE;
/*!40000 ALTER TABLE `cmdb_asset` DISABLE KEYS */;
/*!40000 ALTER TABLE `cmdb_asset` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cmdb_asset_business_line`
--

DROP TABLE IF EXISTS `cmdb_asset_business_line`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cmdb_asset_business_line` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `asset_id` int(11) NOT NULL,
  `businessline_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `cmdb_asset_business_line_asset_id_c8b5a70f_uniq` (`asset_id`,`businessline_id`),
  KEY `cmdb_asset_business_line_51c6d5db` (`asset_id`),
  KEY `cmdb_asset_business_line_c66ad6aa` (`businessline_id`)
) ENGINE=MyISAM AUTO_INCREMENT=83 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cmdb_asset_business_line`
--

LOCK TABLES `cmdb_asset_business_line` WRITE;
/*!40000 ALTER TABLE `cmdb_asset_business_line` DISABLE KEYS */;
/*!40000 ALTER TABLE `cmdb_asset_business_line` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cmdb_businessline`
--

DROP TABLE IF EXISTS `cmdb_businessline`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cmdb_businessline` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `comment` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cmdb_businessline`
--

LOCK TABLES `cmdb_businessline` WRITE;
/*!40000 ALTER TABLE `cmdb_businessline` DISABLE KEYS */;
INSERT INTO `cmdb_businessline` VALUES (13,'业务3','野外'),(12,'业务2','业务2'),(11,'测试','测试');
/*!40000 ALTER TABLE `cmdb_businessline` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cmdb_cpu`
--

DROP TABLE IF EXISTS `cmdb_cpu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cmdb_cpu` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `socket` varchar(20) NOT NULL,
  `family` varchar(10) NOT NULL,
  `version` varchar(80) DEFAULT NULL,
  `speed` varchar(50) NOT NULL,
  `cores` smallint(6) NOT NULL,
  `characteristics` varchar(200) NOT NULL,
  `server_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `cmdb_cpu_5dc6e1b7` (`server_id`)
) ENGINE=MyISAM AUTO_INCREMENT=83 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cmdb_cpu`
--

LOCK TABLES `cmdb_cpu` WRITE;
/*!40000 ALTER TABLE `cmdb_cpu` DISABLE KEYS */;
/*!40000 ALTER TABLE `cmdb_cpu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cmdb_disk`
--

DROP TABLE IF EXISTS `cmdb_disk`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cmdb_disk` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `size` varchar(50) NOT NULL,
  `serialnum` varchar(100) DEFAULT NULL,
  `speed` varchar(50) DEFAULT NULL,
  `manufacturer` varchar(100) DEFAULT NULL,
  `locator` varchar(20) NOT NULL,
  `interface_type` varchar(20) DEFAULT NULL,
  `server_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `cmdb_disk_5dc6e1b7` (`server_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cmdb_disk`
--

LOCK TABLES `cmdb_disk` WRITE;
/*!40000 ALTER TABLE `cmdb_disk` DISABLE KEYS */;
/*!40000 ALTER TABLE `cmdb_disk` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cmdb_history`
--

DROP TABLE IF EXISTS `cmdb_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cmdb_history` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `update_time` datetime NOT NULL,
  `model` varchar(50) NOT NULL,
  `field` varchar(50) NOT NULL,
  `old` varchar(200) DEFAULT NULL,
  `new` varchar(200) DEFAULT NULL,
  `operate` varchar(6) NOT NULL,
  `asset_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `cmdb_history_51c6d5db` (`asset_id`)
) ENGINE=MyISAM AUTO_INCREMENT=543 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cmdb_history`
--

LOCK TABLES `cmdb_history` WRITE;
/*!40000 ALTER TABLE `cmdb_history` DISABLE KEYS */;
/*!40000 ALTER TABLE `cmdb_history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cmdb_hwsystem`
--

DROP TABLE IF EXISTS `cmdb_hwsystem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cmdb_hwsystem` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `serialnum` varchar(100) NOT NULL,
  `manufacturer` varchar(100) NOT NULL,
  `product_name` varchar(100) NOT NULL,
  `uuid` varchar(50) DEFAULT NULL,
  `server_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `cmdb_hwsystem_5dc6e1b7` (`server_id`)
) ENGINE=MyISAM AUTO_INCREMENT=70 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cmdb_hwsystem`
--

LOCK TABLES `cmdb_hwsystem` WRITE;
/*!40000 ALTER TABLE `cmdb_hwsystem` DISABLE KEYS */;
/*!40000 ALTER TABLE `cmdb_hwsystem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cmdb_idc`
--

DROP TABLE IF EXISTS `cmdb_idc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cmdb_idc` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `comment` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cmdb_idc`
--

LOCK TABLES `cmdb_idc` WRITE;
/*!40000 ALTER TABLE `cmdb_idc` DISABLE KEYS */;
INSERT INTO `cmdb_idc` VALUES (1,'内网','内网机房'),(6,'机房3','机房3'),(5,'机房2','机房2'),(7,'机房4','机房4');
/*!40000 ALTER TABLE `cmdb_idc` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cmdb_memory`
--

DROP TABLE IF EXISTS `cmdb_memory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cmdb_memory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `serialnum` varchar(100) DEFAULT NULL,
  `part_number` varchar(100) DEFAULT NULL,
  `speed` varchar(50) NOT NULL,
  `manufacturer` varchar(100) DEFAULT NULL,
  `locator` varchar(20) NOT NULL,
  `size` varchar(20) NOT NULL,
  `server_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `cmdb_memory_5dc6e1b7` (`server_id`)
) ENGINE=MyISAM AUTO_INCREMENT=357 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cmdb_memory`
--

LOCK TABLES `cmdb_memory` WRITE;
/*!40000 ALTER TABLE `cmdb_memory` DISABLE KEYS */;
/*!40000 ALTER TABLE `cmdb_memory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cmdb_networkdevice`
--

DROP TABLE IF EXISTS `cmdb_networkdevice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cmdb_networkdevice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `manufacturer` varchar(200) DEFAULT NULL,
  `product_name` varchar(200) NOT NULL,
  `ip` char(39) DEFAULT NULL,
  `mac` varchar(50) DEFAULT NULL,
  `asset_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `asset_id` (`asset_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cmdb_networkdevice`
--

LOCK TABLES `cmdb_networkdevice` WRITE;
/*!40000 ALTER TABLE `cmdb_networkdevice` DISABLE KEYS */;
/*!40000 ALTER TABLE `cmdb_networkdevice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cmdb_networkinterface`
--

DROP TABLE IF EXISTS `cmdb_networkinterface`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cmdb_networkinterface` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `mac` varchar(50) NOT NULL,
  `ip` char(39) DEFAULT NULL,
  `state` smallint(6) NOT NULL,
  `server_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `cmdb_networkinterface_9ed39e2e` (`state`),
  KEY `cmdb_networkinterface_5dc6e1b7` (`server_id`)
) ENGINE=MyISAM AUTO_INCREMENT=234 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cmdb_networkinterface`
--

LOCK TABLES `cmdb_networkinterface` WRITE;
/*!40000 ALTER TABLE `cmdb_networkinterface` DISABLE KEYS */;
/*!40000 ALTER TABLE `cmdb_networkinterface` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cmdb_server`
--

DROP TABLE IF EXISTS `cmdb_server`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cmdb_server` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hostname` varchar(100) NOT NULL,
  `lan_ip` char(39) NOT NULL,
  `wan_ip` char(39) DEFAULT NULL,
  `logical_cpu` varchar(100) NOT NULL,
  `logical_disk` varchar(50) NOT NULL,
  `logical_memory` varchar(50) NOT NULL,
  `os` varchar(100) NOT NULL,
  `phost_ip` char(39) DEFAULT NULL,
  `asset_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `lan_ip` (`lan_ip`),
  UNIQUE KEY `asset_id` (`asset_id`)
) ENGINE=MyISAM AUTO_INCREMENT=70 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cmdb_server`
--

LOCK TABLES `cmdb_server` WRITE;
/*!40000 ALTER TABLE `cmdb_server` DISABLE KEYS */;
/*!40000 ALTER TABLE `cmdb_server` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cmdb_user`
--

DROP TABLE IF EXISTS `cmdb_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cmdb_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(20) NOT NULL,
  `realname` varchar(20) DEFAULT NULL,
  `password` varchar(100) NOT NULL,
  `email` varchar(254) NOT NULL,
  `mobile` varchar(11) DEFAULT NULL,
  `wechat` varchar(12) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=MyISAM AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cmdb_user`
--

LOCK TABLES `cmdb_user` WRITE;
/*!40000 ALTER TABLE `cmdb_user` DISABLE KEYS */;
INSERT INTO `cmdb_user` VALUES (1,'admin','管理员','8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918','admin@cmdb.org',NULL,NULL);
/*!40000 ALTER TABLE `cmdb_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_417f1b1c` (`content_type_id`),
  KEY `django_admin_log_e8701ad4` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=MyISAM AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(2,'auth','group'),(3,'auth','user'),(4,'auth','permission'),(5,'contenttypes','contenttype'),(6,'sessions','session'),(7,'cmdb','idc'),(8,'cmdb','businessline'),(9,'cmdb','user'),(10,'cmdb','asset'),(11,'cmdb','server'),(12,'cmdb','networkdevice'),(13,'cmdb','networkinterface'),(14,'cmdb','memory'),(15,'cmdb','cpu'),(16,'cmdb','disk'),(17,'cmdb','hwsystem'),(18,'cmdb','history');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2017-07-18 05:57:49'),(2,'auth','0001_initial','2017-07-18 05:57:50'),(3,'admin','0001_initial','2017-07-18 05:57:50'),(4,'admin','0002_logentry_remove_auto_add','2017-07-18 05:57:50'),(5,'contenttypes','0002_remove_content_type_name','2017-07-18 05:57:50'),(6,'auth','0002_alter_permission_name_max_length','2017-07-18 05:57:50'),(7,'auth','0003_alter_user_email_max_length','2017-07-18 05:57:50'),(8,'auth','0004_alter_user_username_opts','2017-07-18 05:57:50'),(9,'auth','0005_alter_user_last_login_null','2017-07-18 05:57:50'),(10,'auth','0006_require_contenttypes_0002','2017-07-18 05:57:50'),(11,'auth','0007_alter_validators_add_error_messages','2017-07-18 05:57:50'),(12,'auth','0008_alter_user_username_max_length','2017-07-18 05:57:50'),(13,'sessions','0001_initial','2017-07-18 05:57:50'),(14,'cmdb','0001_initial','2017-07-18 06:00:43'),(15,'cmdb','0002_auto_20170719_1118','2017-07-19 03:18:27'),(16,'cmdb','0002_auto_20170528_1708','2017-07-20 08:55:14'),(17,'cmdb','0003_auto_20170528_2238','2017-07-20 08:55:15');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('rae8w0wv0zq5rwefbikr4u5oez0i3hcm','YTA5MWU2NzhiMTkzYWRiYmNmYWVmMjY1NDcwYjE1NDIyNGY0ZGE2Mzp7InVzZXJuYW1lIjoiYWRtaW4iLCJ1aWQiOjF9','2017-07-20 09:09:41'),('mmhc2wujcucv4evn6m489ruyzv48ruc4','ZGE1NDlkYzIxMWU1YWI2M2EyNjdhYzdmMDUxOGYzNzU3MzRmNDQ3Zjp7InVpZCI6MywidXNlcm5hbWUiOiJoZWJpbmRlIn0=','2017-07-20 05:51:16'),('onmozpon9tcid5u162h4m57qcthhuh4v','ODMwYjJhOGU0NDNhYjY5ZjU0MDdiNzUxNzFmYzUxMjFiMDhlYmJkZjp7InVpZCI6NCwidXNlcm5hbWUiOiJsaWFvaGFpbGluIn0=','2017-07-20 06:14:30'),('thc2nsh534ornbc4wxul8oa3w96zp2zb','ZGE1NDlkYzIxMWU1YWI2M2EyNjdhYzdmMDUxOGYzNzU3MzRmNDQ3Zjp7InVpZCI6MywidXNlcm5hbWUiOiJoZWJpbmRlIn0=','2017-07-20 06:09:11'),('al8rigb4gv7h95cnfaw0fbegmp29g24z','YTA5MWU2NzhiMTkzYWRiYmNmYWVmMjY1NDcwYjE1NDIyNGY0ZGE2Mzp7InVzZXJuYW1lIjoiYWRtaW4iLCJ1aWQiOjF9','2017-07-20 10:06:39'),('m7kxbwfub8uio5yn7qs70hajiqwo8xvl','YTA5MWU2NzhiMTkzYWRiYmNmYWVmMjY1NDcwYjE1NDIyNGY0ZGE2Mzp7InVzZXJuYW1lIjoiYWRtaW4iLCJ1aWQiOjF9','2017-07-21 11:07:28'),('211vty5reh27qn2platlm7pbu9nzh81j','YTA5MWU2NzhiMTkzYWRiYmNmYWVmMjY1NDcwYjE1NDIyNGY0ZGE2Mzp7InVzZXJuYW1lIjoiYWRtaW4iLCJ1aWQiOjF9','2017-09-01 06:16:48');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-08-31 14:18:31
