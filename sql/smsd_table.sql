-- MySQL dump 10.13  Distrib 5.1.49, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: smsd
-- ------------------------------------------------------
-- Server version	5.1.49-3

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
-- Table structure for table `CardNumber`
--

DROP TABLE IF EXISTS `CardNumber`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `CardNumber` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `number` varchar(50) NOT NULL,
  `status` int(11) DEFAULT NULL,
  `lastupdate` timestamp NULL DEFAULT NULL,
  `hourrate` int(11) DEFAULT NULL,
  `dayrate` int(11) DEFAULT NULL,
  `monthrate` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `number` (`number`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `CardSendHistory`
--

DROP TABLE IF EXISTS `CardSendHistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `CardSendHistory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `number_id` int(11) DEFAULT NULL,
  `create_time` timestamp NULL DEFAULT NULL,
  `msg` varchar(500) DEFAULT NULL,
  `dst_number` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `number_id` (`number_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ChannelItem`
--

DROP TABLE IF EXISTS `ChannelItem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ChannelItem` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `desc` varchar(50) DEFAULT NULL,
  `type` varchar(50) NOT NULL,
  `status` int(11) DEFAULT '0',
  `last_update` datetime DEFAULT NULL,
  PRIMARY KEY (`uid`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM AUTO_INCREMENT=64 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ChannelList`
--

DROP TABLE IF EXISTS `ChannelList`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ChannelList` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `desc` varchar(100) DEFAULT NULL,
  `cm1` int(11) DEFAULT '-1',
  `cm2` int(11) DEFAULT '-1',
  `cm3` int(11) DEFAULT '-1',
  `cu1` int(11) DEFAULT '-1',
  `cu2` int(11) DEFAULT '-1',
  `cu3` int(11) DEFAULT '-1',
  `ct1` int(11) DEFAULT '-1',
  `ct2` int(11) DEFAULT '-1',
  `ct3` int(11) DEFAULT '-1',
  PRIMARY KEY (`uid`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `addmsglog`
--

DROP TABLE IF EXISTS `addmsglog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `addmsglog` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `username` char(50) NOT NULL,
  `before_msg_num` int(11) NOT NULL,
  `add_msg_num` int(11) NOT NULL,
  `after_msg_num` int(11) NOT NULL,
  `type` int(11) NOT NULL,
  `create_time` datetime NOT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=MyISAM AUTO_INCREMENT=647 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `addresslist`
--

DROP TABLE IF EXISTS `addresslist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `addresslist` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `user_uid` int(11) NOT NULL,
  `name` char(50) NOT NULL,
  `number` blob NOT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=MyISAM AUTO_INCREMENT=58 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `channelitem`
--

DROP TABLE IF EXISTS `channelitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `channelitem` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `desc` varchar(50) DEFAULT NULL,
  `type` varchar(50) NOT NULL,
  `status` int(11) DEFAULT '0',
  `last_update` datetime DEFAULT NULL,
  PRIMARY KEY (`uid`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `message`
--

DROP TABLE IF EXISTS `message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `message` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `user_uid` int(11) NOT NULL,
  `address` mediumtext,
  `address_list` int(11) DEFAULT NULL,
  `msg` varchar(4000) NOT NULL,
  `msg_num` int(11) NOT NULL,
  `status` int(11) NOT NULL,
  `create_time` datetime NOT NULL,
  `last_update` datetime DEFAULT NULL,
  `channel` varchar(4000) DEFAULT NULL,
  `fail_msg` varchar(4000) DEFAULT NULL,
  `total_num` int(11) DEFAULT NULL,
  `sub_num` int(11) DEFAULT NULL,
  `seed` int(11) DEFAULT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=MyISAM AUTO_INCREMENT=252326 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `phone`
--

DROP TABLE IF EXISTS `phone`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `phone` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `phonebook_uid` int(11) NOT NULL,
  `name` char(50) DEFAULT NULL,
  `companyname` char(50) DEFAULT NULL,
  `title` char(50) DEFAULT NULL,
  `mobile` char(50) NOT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=MyISAM AUTO_INCREMENT=82281 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `phonebook`
--

DROP TABLE IF EXISTS `phonebook`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `phonebook` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `user_uid` int(11) NOT NULL,
  `name` char(50) NOT NULL,
  `remark` blob,
  PRIMARY KEY (`uid`)
) ENGINE=MyISAM AUTO_INCREMENT=291 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `receive_log`
--

DROP TABLE IF EXISTS `receive_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `receive_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `log` varchar(50000) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id` (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sessions`
--

DROP TABLE IF EXISTS `sessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sessions` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `username` char(50) NOT NULL,
  `sid` varchar(4000) NOT NULL,
  `active` int(11) NOT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=MyISAM AUTO_INCREMENT=8915 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `upload_msg`
--

DROP TABLE IF EXISTS `upload_msg`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `upload_msg` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ext` char(50) DEFAULT NULL,
  `number` char(50) DEFAULT NULL,
  `content` varchar(4000) DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id` (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2002 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `username` char(50) NOT NULL,
  `description` char(50) DEFAULT NULL,
  `password` char(40) NOT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `msg_num` int(11) NOT NULL,
  `flags` int(11) DEFAULT NULL,
  `is_active` int(11) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `last_login` datetime DEFAULT NULL,
  `can_weblogin` tinyint(1) DEFAULT NULL,
  `can_post` tinyint(1) DEFAULT NULL,
  `need_check` tinyint(1) DEFAULT NULL,
  `channel_cm` varchar(4000) DEFAULT NULL,
  `channel_cu` varchar(4000) DEFAULT NULL,
  `channel_ct` varchar(4000) DEFAULT NULL,
  `ext` char(50) DEFAULT NULL,
  `percent` int(11) DEFAULT NULL,
  `channel_list_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=MyISAM AUTO_INCREMENT=226 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2011-11-26 18:52:56
