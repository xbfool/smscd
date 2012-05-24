package com.xbfool.smsc.event
{
	import flash.events.Event;
	
	public class CompRetEvent extends Event
	{
		static public const COMP_RET:String = 'comp_ret';

		public function CompRetEvent(type:String)
		{

			super(type, bubbles, cancelable);
		}
		
		override public function clone():Event
		{
			return new CompRetEvent(this.type);
		}
	}
}