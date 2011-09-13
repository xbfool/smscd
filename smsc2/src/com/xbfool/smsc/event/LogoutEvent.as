package com.xbfool.smsc.event
{
	import flash.events.Event;
	
	public class LogoutEvent extends Event
	{
		static public const LOGOUT:String = 'logout';
		

		public function LogoutEvent(type:String)
		{	
			super(type);
		}
		
		override public function clone():Event
		{
			return new LogoutEvent(this.type);
		}
	}
}