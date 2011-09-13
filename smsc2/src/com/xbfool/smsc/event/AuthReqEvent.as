package com.xbfool.smsc.event
{	
	
	import flash.events.Event;
	
	public class AuthReqEvent extends Event
	{
		static public const AUTH_REQ:String = 'auth_req';
		
		public var userName: String;
		public var passWord: String;
		public var errno: int;
		
		public function AuthReqEvent(type:String,
								  userName:String='',
								  passWord:String='',
								  errno:int=0)
		{
			this.userName = userName;
			this.passWord = passWord;
			this.errno = errno;
			super(type)
		}
		
		override public function clone():Event
		{
			return new AuthReqEvent(this.type,
								 this.userName,
								 this.passWord,
								 this.errno);
		}
	}
}