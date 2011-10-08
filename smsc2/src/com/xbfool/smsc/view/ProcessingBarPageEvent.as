// ActionScript file
package com.xbfool.smsc.view
{
	import flash.events.Event;
	
	public class ProcessingBarPageEvent extends Event
	{
		public static const PROCESSING_BAR_PAGE_CLOSE:String = 'process_bar_page_close';
		public static const PROCESSING_BAR_PAGE_ADD:String = 'process_bar_page_add';
		public function ProcessingBarPageEvent(type:String)
		{
			super(type, true);
		}
		
	}
}