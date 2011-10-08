// ActionScript file
package com.xbfool.smsc.event
{	
	
	import flash.events.Event;
	
	public class ChannelItemEvent extends Event
	{
		static public const CHANNEL_ITEM_ADD:String = 'channel_item_add';
		static public const CHANNEL_ITEM_QUERY_RET:String = 'channel_item_query_ret';
		static public const CHANNEL_ITEM_QUERY_REQ:String = 'channel_item_query_req';
		public var name: String;
		public var desc: String;
		public var ctype: String;
		public var errno: int;
		public var query_ret_object: Object;
		
		public function ChannelItemEvent(type:String,
											name:String="",
											desc:String="",
											ctype:String="",
									 		errno:int=0,
											query_ret_ojbect:Object=null)
		{
			this.name = name;
			this.desc = desc;
			this.ctype = ctype;
			this.errno = errno;
			this.query_ret_object = query_ret_ojbect
			super(type);
		}
		
		override public function clone():Event
		{
			return new ChannelItemEvent(this.type,
				this.name,
				this.desc,
				this.ctype,
				this.errno,
				this.query_ret_object);
		}
	}
}