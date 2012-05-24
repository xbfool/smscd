package com.xbfool.smsc.event
{	
	
	import flash.events.Event;
	
	public class CompReqEvent extends Event
	{
		static public const CompReq:String = 'comp_req';
		
		public var request_list:Array;
		public function CompReqEvent(type:String, request_list:Array)
		{
			this.request_list = request_list;
			super(type)
		}
		
		override public function clone():Event
		{
			return new CompReqEvent(this.type, request_list);
		}
	}
}