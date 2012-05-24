package com.xbfool.smsc.event
{	
	
	import flash.events.Event;
	
	public class ProcessingEvent extends Event
	{
		static public const PROCESSING_BEGIN:String = 'processing_begin';
		static public const PROCESSING_END:String = 'processing_end';
		public function ProcessingEvent(type:String)
		{
			super(type)
		}
		
		override public function clone():Event
		{
			return new ProcessingEvent(this.type);
		}
	}
}