// ActionScript file
package com.xbfool.smsc.controller
{
	import flash.events.Event;
	
	public class RequestEvent extends Event
	{
		public static const AUTH:String = 'auth';

		public var param:Object;
		
		public static function CheckType(type:String):Boolean {
			var list:Object = {
				'auth':'auth'
			};
				
			if(list[type] != null)
				return true;
			else
				return false;
		}
		public function RequestEvent(type:String, param:Object=null)
		{
			this.param = param;
			super(type,true,true);
		}
		
		public override function clone() : Event
		{
			return new RequestEvent(this.type, this.param);
		}
		
		public override function toString():String
		{
			return formatToString("RequestEvent", "param", "type", "bubbles", "cancelable");
		}

	}
}