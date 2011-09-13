// ActionScript file
package com.xbfool.smsc.event
{
	import flash.events.Event;
	
	public class RetEvent extends Event
	{
		static public const RET:String = 'ret';
		
		public var param:Object;
		
		public function RetEvent(type:String,
									 param:Object=null)
		{	
			this.param = param;
			super(type);
		}
		
		override public function clone():Event
		{
			return new RetEvent(this.type,
				this.param);
		}
	}
}