package com.xbfool.smsc.view
{
	import flash.events.Event;
	
	public class MessageSendPageEvent extends Event
	{
		public static const CLEAN:String = 'clean';
		public static const MESSAGE_CHANGE:String = 'message_change';
		public static const ADD_ADDRESS:String = 'add_address';
		public static const ADDRESS_CHANGE:String = 'address_change';
		public static const FILTER_ADDRESS:String = 'filter_address';
		public static const DEL_ONE_ADDRESS:String = 'del_one_address';
		public static const CLEAN_ALL_ADDRESS:String = 'clean_all_address';
		public static const SAVE_ADDRESS:String = 'save_address';
		public static const IMPORT_ADDRESS_FILE:String = 'import_address_file';
		public static const SEND_MESSAGE:String = 'send_message';
		public function MessageSendPageEvent(type:String)
		{
			super(type);
		}
	}
}