DELIMITER $$

USE `smsd`$$

DROP PROCEDURE IF EXISTS `message_report`$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `message_report`(
    	username CHAR(50),
	begindate DATETIME,
	enddate DATETIME
	)
BEGIN
	IF (username <> '') THEN 
	   SELECT DISTINCT 
	   U.username AS NAME,
	   (SELECT SUM(message.msg_num) FROM message) AS totalMsg,
	   (SELECT SUM(message.msg_num) FROM message WHERE STATUS=1 ) AS success,
	   (SELECT SUM(message.msg_num) FROM message WHERE STATUS=0 ) AS failure,
	   (SELECT SUM(message.msg_num) FROM message WHERE STATUS=0 AND create_time = last_update) AS append
	   FROM USER U, message M
	   WHERE  U.username=username AND  U.uid = M.user_uid AND begindate < M.last_update AND M.last_update < enddate;
	ELSE 	
	   SELECT DISTINCT 
	   U.username AS NAME,
	   (SELECT SUM(message.msg_num) FROM message) AS totalMsg,
	   (SELECT SUM(message.msg_num) FROM message WHERE STATUS=1 ) AS success,
	   (SELECT SUM(message.msg_num) FROM message WHERE STATUS=0 ) AS failure,
	  (SELECT SUM(message.msg_num) FROM message WHERE STATUS=0 AND create_time = last_update) AS append
	   FROM USER U, message M
	   WHERE  U.uid = M.user_uid AND begindate < M.last_update AND M.last_update < enddate;
	END IF;	
    END$$
    
DELIMITER ;
