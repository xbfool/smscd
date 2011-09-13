// ActionScript file
// ActionScript file
package com.xbfool.smsc.view
{
	import flash.events.Event;
	
	public class MainPageEvent extends Event
	{
		public static const LOGOUT:String = 'logout';

		public function MainPageEvent(type:String)
		{
			super(type, true);
		}
		
	}
}