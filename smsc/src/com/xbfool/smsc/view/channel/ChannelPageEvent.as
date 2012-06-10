// ActionScript file
package com.xbfool.smsc.view.channel
{
	import flash.events.Event;
	
	public class ChannelPageEvent extends Event
	{
		public static const CHANNEL_ITEM_ADD_PAGE:String = 'channel_item_add_page';
		public static const CHANNEL_ITEM_QUERY:String = 'channel_item_query';
		public static const CHANNEL_ITEM_DELETE:String = 'channel_item_delete';
		public static const CHANNEL_ITEM_UPDATE:String = 'channel_item_update';
		public static const CHANNEL_ITEM_ADD_ITEM:String = 'channel_item_add_item';
		public static const CHANNEL_ITEM_START:String = 'channel_item_start';
		public static const CHANNEL_ITEM_STOP:String = 'channel_item_stop';
		public static const CHANNEL_LIST_ADD_PAGE:String = 'channel_list_add_page';
		public static const CHANNEL_LIST_ADD_ITEM:String = 'channel_list_add_item';
		public static const CHANNEL_LIST_DELETE:String = 'channel_list_delete';
		public static const CHANNEL_LIST_UPDATE:String = 'channel_list_update';
		public static const USER_CHANNEL_LIST_USE_NONE:String = 'user_channel_list_use_none';
		public static const USER_CHANNEL_LIST_UPDATE:String = 'user_channel_list_update';
		public function ChannelPageEvent(type:String)
		{
			super(type, true);
		}
		
	}
}