// ActionScript file
// ActionScript file
package com.xbfool.smsc.view
{
	import flash.events.Event;
	
	public class MainPageEvent extends Event
	{
		public static const LOGOUT:String = 'logout';
		public static const MESSAGE_SEND_VIEW:String = 'message_send_view';
		public static const SPECIAL_SEND_VIEW:String = 'special_send_view';
		public static const MESSAGE_LOG_VIEW:String = 'message_log_view';
		public static const MESSAGE_CHART_VIEW:String = 'message_chart_view';
		public static const MONEY_LOG_VIEW:String = 'money_log_view';
		public static const MANAGE_ADDRESS_VIEW:String = 'manage_address_view';
		public static const UPLOAD_MESSAGE_VIEW:String = 'upload_message_view';
		public static const CHANNEL_LOG_VIEW:String ='channel_log_view';
		public static const MANAGE_USER_VIEW:String = 'manage_user_view';
		public static const CHANGE_PASSWORD_VIEW:String = 'change_password_button';
		
		public function MainPageEvent(type:String)
		{
			super(type, true);
		}
		
	}
}