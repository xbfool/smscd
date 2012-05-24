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
		
		public static function checkAddressValid(address:String):Boolean {
			if(address.length != 11 || address.charAt(0) != '1' 
				|| (address.charAt(1) != '3' &&
					address.charAt(1) != '4' &&
					address.charAt(1) != '5' &&
					address.charAt(1) != '8'
				))
			{
				return false;
			} else
				return true;
		}
	}
}