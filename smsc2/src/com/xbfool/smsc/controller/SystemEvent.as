// ActionScript file
package com.xbfool.smsc.controller
{
	import flash.events.Event;
	
	public class SystemEvent extends Event
	{
		public static const LOG_OUT:String = 'logOut';
		
		public function SystemEvent(type:String)
		{
			super(type);
		}
		
		override public function clone():Event
		{
			return new SystemEvent(type);
		}
		
	}
}