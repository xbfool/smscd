// ActionScript file
package com.xbfool.smsc.view
{
	import flash.events.Event;
	
	public class ChannelItemPageEvent extends Event
	{
		public static const CHANNEL_ITEM_ADD_PAGE:String = 'channel_item_add_page';
		public static const CHANNEL_ITEM_QUERY:String = 'channel_item_query';
		public static const CHANNEL_ITEM_DELETE:String = 'channel_item_delete';
		public static const CHANNEL_ITEM_UPDATE:String = 'channel_item_update';
		public static const CHANNEL_ITEM_ADD_ITEM:String = 'channel_item_add_item';
		public function ChannelItemPageEvent(type:String)
		{
			super(type, true);
		}
		
	}
}