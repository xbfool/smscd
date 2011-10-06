// ActionScript file
package com.xbfool.smsc.command
{
	import com.xbfool.smsc.controller.*;
	import com.xbfool.smsc.services.*;
	import com.xbfool.smsc.event.*;
	import org.robotlegs.mvcs.Command;
	import com.adobe.crypto.SHA1;
	
		public class AuthReqCommand extends Command
		{
			[Inject]
			public var event:AuthReqEvent;
			[Inject]
			public var reqestService:IRequestService;

			override public function execute():void
			{
				reqestService.request({command:'user_login', username:event.userName, password:SHA1.hash(event.passWord)});
			}
			
		}
}