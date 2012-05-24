package com.xbfool.smsc.event
{
	import flash.events.Event;
	
	public class SendMessageEvent extends Event
	{
		static public const SEND_MESSAGE:String = 'send_message';
		
		public var sid:String;
		public var address:Array;
		public var address_list:int;
		public var msgContent:String;
		public var addressType:int;
		public var remain:int;
		
		public function SendMessageEvent(type:String,
			sid:String,
			address:Array,
			msgContent:String,
			address_list:int = 0,
			addressType:int = 0,
			remain:int = 0;
		{
			super(type);
		}
		
		override public function clone():Event
		{
			return new AuthReqEvent(this.type,
				this.sid,
				this.address,
				this.msgContent,
				this.address_list,
				this.addressType,
				this.remain);
		}
	}
	
}