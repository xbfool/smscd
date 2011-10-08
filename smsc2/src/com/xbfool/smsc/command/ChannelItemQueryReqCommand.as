package com.xbfool.smsc.command
{
	import com.xbfool.smsc.controller.*;
	import com.xbfool.smsc.services.*;
	import com.xbfool.smsc.event.*;
	import org.robotlegs.mvcs.Command;
	
	public class ChannelItemQueryReqCommand extends Command
	{
		[Inject]
		public var event:ChannelItemEvent;
		[Inject]
		public var reqestService:IRequestService;
		
		public function ChannelItemQueryReqCommand()
		{
			reqestService.request({command:'channel_item_query'});
		}
	}
}