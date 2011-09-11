-- MySQL dump 10.11
--
-- Host: localhost    Database: smsd
-- ------------------------------------------------------
-- Server version	5.0.77

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
-- Table structure for table `addmsglog`
--

DROP TABLE IF EXISTS `addmsglog`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `addmsglog` (
  `uid` int(11) NOT NULL auto_increment,
  `username` char(50) NOT NULL,
  `before_msg_num` int(11) NOT NULL,
  `add_msg_num` int(11) NOT NULL,
  `after_msg_num` int(11) NOT NULL,
  `type` int(11) NOT NULL,
  `create_time` datetime NOT NULL,
  PRIMARY KEY  (`uid`)
) ENGINE=MyISAM AUTO_INCREMENT=409 DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `addresslist`
--

DROP TABLE IF EXISTS `addresslist`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `addresslist` (
  `uid` int(11) NOT NULL auto_increment,
  `user_uid` int(11) NOT NULL,
  `name` char(50) NOT NULL,
  `number` blob NOT NULL,
  PRIMARY KEY  (`uid`)
) ENGINE=MyISAM AUTO_INCREMENT=58 DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `message`
--

DROP TABLE IF EXISTS `message`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `message` (
  `uid` int(11) NOT NULL auto_increment,
  `user_uid` int(11) NOT NULL,
  `address` mediumtext,
  `address_list` int(11) default NULL,
  `msg` varchar(4000) NOT NULL,
  `msg_num` int(11) NOT NULL,
  `status` int(11) NOT NULL,
  `create_time` datetime NOT NULL,
  `last_update` datetime default NULL,
  `channel` varchar(4000) default NULL,
  `fail_msg` varchar(4000) default NULL,
  `total_num` int(11) default NULL,
  `sub_num` int(11) default NULL,
  `seed` int(11) default NULL,
  PRIMARY KEY  (`uid`)
) ENGINE=MyISAM AUTO_INCREMENT=183845 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `phone`
--

DROP TABLE IF EXISTS `phone`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `phone` (
  `uid` int(11) NOT NULL auto_increment,
  `phonebook_uid` int(11) NOT NULL,
  `name` char(50) default NULL,
  `companyname` char(50) default NULL,
  `title` char(50) default NULL,
  `mobile` char(50) NOT NULL,
  PRIMARY KEY  (`uid`)
) ENGINE=MyISAM AUTO_INCREMENT=60575 DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `phonebook`
--

DROP TABLE IF EXISTS `phonebook`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `phonebook` (
  `uid` int(11) NOT NULL auto_increment,
  `user_uid` int(11) NOT NULL,
  `name` char(50) NOT NULL,
  `remark` blob,
  PRIMARY KEY  (`uid`)
) ENGINE=MyISAM AUTO_INCREMENT=212 DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `receive_log`
--

DROP TABLE IF EXISTS `receive_log`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `receive_log` (
  `id` int(11) NOT NULL auto_increment,
  `log` varchar(50000) default NULL,
  PRIMARY KEY  (`id`),
  KEY `id` (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `sessions`
--

DROP TABLE IF EXISTS `sessions`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `sessions` (
  `uid` int(11) NOT NULL auto_increment,
  `username` char(50) NOT NULL,
  `sid` varchar(4000) NOT NULL,
  `active` int(11) NOT NULL,
  PRIMARY KEY  (`uid`)
) ENGINE=MyISAM AUTO_INCREMENT=5907 DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `upload_msg`
--

DROP TABLE IF EXISTS `upload_msg`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `upload_msg` (
  `id` int(11) NOT NULL auto_increment,
  `ext` char(50) default NULL,
  `number` char(50) default NULL,
  `content` varchar(4000) default NULL,
  `time` datetime default NULL,
  PRIMARY KEY  (`id`),
  KEY `id` (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1107 DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `user` (
  `uid` int(11) NOT NULL auto_increment,
  `username` char(50) NOT NULL,
  `description` char(50) default NULL,
  `password` char(40) NOT NULL,
  `parent_id` int(11) default NULL,
  `msg_num` int(11) NOT NULL,
  `flags` int(11) default NULL,
  `is_active` int(11) default NULL,
  `create_time` datetime default NULL,
  `last_login` datetime default NULL,
  `can_weblogin` tinyint(1) default NULL,
  `can_post` tinyint(1) default NULL,
  `need_check` tinyint(1) default NULL,
  `channel_cm` varchar(4000) default NULL,
  `channel_cu` varchar(4000) default NULL,
  `channel_ct` varchar(4000) default NULL,
  `ext` char(50) default NULL,
  `percent` int(11) default NULL,
  PRIMARY KEY  (`uid`)
) ENGINE=MyISAM AUTO_INCREMENT=179 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2011-09-11 11:50:39
