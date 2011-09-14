package com.xbfool.smsc.utils
{
	public class MessageUtil
	{
		public function MessageUtil()
		{
		}
		
		public static function computeMessageNum(msg:String, address_num:int = 1):Object
		{
			var strLen:int = msg.length;
			var msgNum:int = 0;
			if(strLen == 0)
				msgNum = 0;
			else if(strLen <= 70)
				msgNum = 1;
			else
				msgNum = (strLen - 1) / 65 + 1;
			
			var totalNum:int = msgNum * address_num;
			return {msgCharCount:strLen,
					addressNum:address_num,
					totalNum:totalNum,
					splitNum:msgNum};
		}
	}
}