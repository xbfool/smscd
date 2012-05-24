// ActionScript file
package com.xbfool.smsc.command
{
	import com.xbfool.smsc.controller.*;
	import com.xbfool.smsc.services.*;
	import com.xbfool.smsc.event.*;
	import org.robotlegs.mvcs.Command;
	import com.adobe.crypto.SHA1;
	
	public class CompReqCommand extends Command
	{
		[Inject]
		public var event:CompReqEvent;
		[Inject]
		public var reqestService:IRequestService;
		
		override public function execute():void
		{
			reqestService.request({command:'comp_req', request_list:event.request_list});
		}
		
	}
}