// ActionScript file
package com.xbfool.smsc.command
{
	import com.adobe.crypto.SHA1;
	import com.xbfool.smsc.controller.*;
	import com.xbfool.smsc.event.*;
	import com.xbfool.smsc.services.*;
	
	import org.robotlegs.mvcs.Command;
	
		public class AuthReqCommand extends Command
		{
			[Inject]
			public var event:AuthReqEvent;
			[Inject]
			public var reqestService:IRequestService;

			override public function execute():void
			{
				var request_list:Array = [{command:'user_login', username:event.userName, password:SHA1.hash(event.passWord)},
										   {command:'channel_item_query_all'},
										   {command:'channel_list_query_all'},
										   {command:'user_query_all'}];
					
				
				
				dispatch(new CompReqEvent(CompReqEvent.CompReq, request_list));
				//reqestService.request({command:'user_login', username:event.userName, password:SHA1.hash(event.passWord)});
			}
			
		}
}