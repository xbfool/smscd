package com.xbfool.smsc.event
{
	import flash.events.Event;
	
	public class CompRetEvent extends Event
	{
		static public const COMP_RET:String = 'compret';
		public var ret:Object;
		public var errno:int;
		public function CompRetEvent(type:String, errno:int, ret:Object)
		{
			this.errno = errno;
			this.ret = ret;
			super(type, bubbles, cancelable);
		}
		
		override public function clone():Event
		{
			return new CompRetEvent(this.type, this.errno, this.ret);
		}
	}
}