CREATE TABLE `upload_url` (
  `user_uid` int(11) NOT NULL,
  `url` mediumtext,
  `last_update` datetime default NULL,
  PRIMARY KEY  (`user_uid`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;