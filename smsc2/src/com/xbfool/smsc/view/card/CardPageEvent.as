// ActionScript file
package com.xbfool.smsc.view.card
{
	import flash.events.Event;
	
	public class CardPageEvent extends Event
	{
		public static const CARD_ITEM_ADD_PAGE:String = 'card_item_add_page';
		public static const CARD_ITEM_ADD_ITEM:String = 'card_item_add_item';
		public function CardPageEvent(type:String)
		{
			super(type, true);
		}
		
	}
}