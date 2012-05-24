package com.xbfool.smsc.event
{
	import flash.events.Event;
	
	public class AuthRetEvent extends Event
	{
		static public const AUTH_RET:String = 'auth_ret';
		
		public var userName:String;
		public var sessionId:String;
		public var errno:int;
		public function AuthRetEvent(type:String,
									 userName:String='',
									 sessionId:String='',
									 errno:int=0)
		{	
			this.userName = userName;
			this.sessionId = sessionId;
			this.errno = errno;
			super(type);
		}
		
		override public function clone():Event
		{
			return new AuthRetEvent(this.type,
				this.userName,
				this.sessionId,
				this.errno);
		}
	}
}