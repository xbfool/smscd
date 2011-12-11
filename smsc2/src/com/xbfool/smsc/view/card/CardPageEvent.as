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
		
		public function CardPageEvent(type:String)
		{
			super(type, true);
		}
		
	}
}