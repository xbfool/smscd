package com.xbfool.smsc.view
{
	import flash.events.Event;
	
	public class MessageSendPageEvent extends Event
	{
		public static const CLEAN:String = 'clean';
		public static const MESSAGE_CHANGE:String = 'message_change';
		public function MessageSendPageEvent(type:String)
		{
			super(type);
		}
	}
}