CREATE TABLE `smsd`.`user`
(
uid INT NOT NULL AUTO_INCREMENT,
username CHAR(50) NOT NULL,
description CHAR(50),
password CHAR(40) NOT NULL,
parent_id INT,
msg_num INT NOT NULL,
flags INT,
is_active INT,
create_time DATETIME,
last_login DATETIME,
can_weblogin BOOL,
can_post BOOL,
need_check BOOL,
channel_cm varchar(4000),
channel_cu varchar(4000),
channel_ct varchar(4000),
ext CHAR(50),
PRIMARY KEY (uid)
)DEFAULT CHARSET=utf8 ;

CREATE TABLE `smsd`.`message`
(
uid INT NOT NULL AUTO_INCREMENT,
user_uid INT NOT NULL,
address VARCHAR(40000) NOT NULL,
address_list INT,
msg VARCHAR(4000) NOT NULL,
msg_num INT NOT NULL,
status INT NOT NULL,
create_time DATETIME NOT NULL,
last_update DATETIME,
channel varchar(4000),
fail_msg varchar(4000),
PRIMARY KEY (uid)
)DEFAULT CHARSET=utf8 ;
create table `smsd`.`sessions`
(
uid INT NOT NULL AUTO_INCREMENT,
username CHAR(50) NOT NULL,
sid varchar(4000) NOT NULL,
active INT NOT NULL,
PRIMARY KEY (uid)
)DEFAULT CHARSET=utf8 ;

CREATE TABLE `smsd`.`addmsglog`
(
uid INT NOT NULL AUTO_INCREMENT,
username char(50) NOT NULL,
before_msg_num INT NOT NULL,
add_msg_num INT NOT NULL,
after_msg_num INT NOT NULL,
type INT NOT NULL,
create_time DATETIME NOT NULL,
PRIMARY KEY (uid)
)DEFAULT CHARSET=utf8 ;

CREATE TABLE `smsd`.`addresslist`
(
uid INT NOT NULL AUTO_INCREMENT,
user_uid INT NOT NULL,
name char(50) NOT NULL,
number BLOB NOT NULL,
PRIMARY KEY(uid)
)DEFAULT CHARSET=utf8 ;

create table `smsd`.`phonebook`
(
uid int not null auto_increment,
user_id int not null,
name char(50) not null,
remark BLOB,
primary key(uid)
)default charset=utf8;

create table `smsd`.`phone`
(
uid int not null auto_increment,
phonebook_id int not null,
name char(50),
companyname char(50),
title char(50),
mobile char(50) not null,
primary key(uid)
)DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `smsd`.`receive_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `log` varchar(50000) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id` (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

CREATE TABLE IF NOT EXISTS `upload_msg` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ext` char(10) CHARACTER SET utf8 DEFAULT NULL,
  `number` char(50) CHARACTER SET utf8 DEFAULT NULL,
  `content` varchar(4000) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id` (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;
