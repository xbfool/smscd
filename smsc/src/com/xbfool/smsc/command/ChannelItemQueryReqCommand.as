// ActionScript file
package com.xbfool.smsc.command
{
	import com.adobe.crypto.SHA1;
	import com.xbfool.smsc.controller.*;
	import com.xbfool.smsc.event.*;
	import com.xbfool.smsc.model.UserProxy;
	import com.xbfool.smsc.services.*;
	
	import org.robotlegs.mvcs.Command;
	
	public class ChannelItemQueryReqCommand extends Command
	{
		[Inject]
		public var event:ChannelItemEvent;
		[Inject]
		public var reqestService:IRequestService;
		[Inject]
		public var userProxy:UserProxy;
		
		override public function execute():void
		{
			//TODO
			reqestService.request({command:'channel_item_query_all'});
		}
		
	}
}