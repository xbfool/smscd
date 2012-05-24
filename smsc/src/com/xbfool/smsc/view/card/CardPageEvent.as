// ActionScript file
package com.xbfool.smsc.view.card
{
	import flash.events.Event;
	
	public class CardPageEvent extends Event
	{
		public static const CARD_ITEM_ADD_PAGE:String = 'card_item_add_page';
		public static const CARD_ITEM_ADD_ITEM:String = 'card_item_add_item';
		public static const CARD_ITEM_UPDATE:String = 'card_item_update';
		public static const CARD_ITEM_DELETE:String = 'card_item_delete';
		public static const CARD_ITEM_QUERY:String = 'card_item_query';
		public static const CARD_ITEM_ADD_LIST:String = 'card_item_add_list';
		public static const CARD_ITEM_DOWNLOAD_TEMPLATE:String = 'card_item_download_template';
		public static const CARD_ITEM_ADD_LIST_COMMIT:String = 'card_item_add_list_commit';
		
		public function CardPageEvent(type:String)
		{
			super(type, true);
		}
		
	}
}