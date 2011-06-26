-- phpMyAdmin SQL Dump
-- version 3.3.9
-- http://www.phpmyadmin.net
--
-- 主机: localhost
-- 生成日期: 2011 年 06 月 26 日 15:56
-- 服务器版本: 5.5.8
-- PHP 版本: 5.3.5

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- 数据库: `smsd`
--

-- --------------------------------------------------------

--
-- 表的结构 `addmsglog`
--

CREATE TABLE IF NOT EXISTS `addmsglog` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `username` char(50) NOT NULL,
  `before_msg_num` int(11) NOT NULL,
  `add_msg_num` int(11) NOT NULL,
  `after_msg_num` int(11) NOT NULL,
  `type` int(11) NOT NULL,
  `create_time` datetime NOT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

--
-- 转存表中的数据 `addmsglog`
--


-- --------------------------------------------------------

--
-- 表的结构 `addresslist`
--

CREATE TABLE IF NOT EXISTS `addresslist` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `user_uid` int(11) NOT NULL,
  `name` char(50) NOT NULL,
  `number` blob NOT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

--
-- 转存表中的数据 `addresslist`
--


-- --------------------------------------------------------

--
-- 表的结构 `message`
--

CREATE TABLE IF NOT EXISTS `message` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `user_uid` int(11) NOT NULL,
  `address` mediumtext NOT NULL,
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
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=22 ;

--
-- 转存表中的数据 `message`
--


-- --------------------------------------------------------

--
-- 表的结构 `phone`
--

CREATE TABLE IF NOT EXISTS `phone` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `phonebook_uid` int(11) NOT NULL,
  `name` char(50) DEFAULT NULL,
  `companyname` char(50) DEFAULT NULL,
  `title` char(50) DEFAULT NULL,
  `mobile` char(50) NOT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

--
-- 转存表中的数据 `phone`
--


-- --------------------------------------------------------

--
-- 表的结构 `phonebook`
--

CREATE TABLE IF NOT EXISTS `phonebook` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `user_uid` int(11) NOT NULL,
  `name` char(50) NOT NULL,
  `remark` blob,
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

--
-- 转存表中的数据 `phonebook`
--


-- --------------------------------------------------------

--
-- 表的结构 `receive_log`
--

CREATE TABLE IF NOT EXISTS `receive_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `log` varchar(50000) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id` (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- 转存表中的数据 `receive_log`
--


-- --------------------------------------------------------

--
-- 表的结构 `sessions`
--

CREATE TABLE IF NOT EXISTS `sessions` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `username` char(50) NOT NULL,
  `sid` varchar(4000) NOT NULL,
  `active` int(11) NOT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=29 ;

--
-- 转存表中的数据 `sessions`
--

-- --------------------------------------------------------

--
-- 表的结构 `upload_msg`
--

CREATE TABLE IF NOT EXISTS `upload_msg` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ext` char(50) DEFAULT NULL,
  `number` char(50) DEFAULT NULL,
  `content` varchar(4000) DEFAULT NULL,
  `time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id` (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;

--
-- 转存表中的数据 `upload_msg`
--

-- --------------------------------------------------------

--
-- 表的结构 `user`
--

CREATE TABLE IF NOT EXISTS `user` (
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
  `percent` int(11) NOT NULL DEFAULT '100',
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=5 ;

--
-- 转存表中的数据 `user`
--