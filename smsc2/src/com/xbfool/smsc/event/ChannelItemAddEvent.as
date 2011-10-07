// ActionScript file
package com.xbfool.smsc.event
{	
	
	import flash.events.Event;
	
	public class ChannelItemAddEvent extends Event
	{
		static public const CHANNEL_ITEM_ADD:String = 'channel_item_add';
		
		public var name: String;
		public var desc: String;
		public var ctype: String;
		public var errno: int;
		public function ChannelItemAddEvent(type:String,
											name:String,
											desc:String,
											ctype:String,
									 		errno:int=0)
		{
			this.name = name;
			this.desc = desc;
			this.ctype = ctype;
			this.errno = errno;
			super(type);
		}
		
		override public function clone():Event
		{
			return new ChannelItemAddEvent(this.type,
				this.name,
				this.desc,
				this.ctype,
				this.errno);
		}
	}
}