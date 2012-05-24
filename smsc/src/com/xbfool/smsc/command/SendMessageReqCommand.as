// ActionScript file
// ActionScript file
package com.xbfool.smsc.command
{
	import com.adobe.crypto.SHA1;
	import com.xbfool.smsc.controller.*;
	import com.xbfool.smsc.event.*;
	import com.xbfool.smsc.model.UserProxy;
	import com.xbfool.smsc.services.*;
	
	import org.robotlegs.mvcs.Command;
	
	public class SendMessageReqCommand extends Command
	{
		[Inject]
		public var userProxy:UserProxy;
		[Inject]
		public var event:SendMessageEvent;
		[Inject]
		public var reqestService:IRequestService;
		
		override public function execute():void
		{
			while(event.address.length > 0){
				var tmpAddress:Array = event.address.splice(0, 1000);
				reqestService.request({q:'sendmessage', sid:userProxy.sessionId, 
					address:tmpAddress.join(), address_list:0, 
					msg:event.msgContent, type:event.addressType, remain:event.remain});
			}
		}
		
	}
}