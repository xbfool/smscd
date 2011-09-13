// ActionScript file
// ActionScript file
// ActionScript file
package com.xbfool.smsc.command
{
	import com.adobe.crypto.SHA1;
	import com.xbfool.smsc.controller.*;
	import com.xbfool.smsc.event.*;
	import com.xbfool.smsc.services.*;
	
	import org.robotlegs.mvcs.Command;
	
	public class RetCommand extends Command
	{
		[Inject]
		public var event:RetEvent;
		[Inject]
		public var reqestService:IRequestService;
		
		override public function execute():void
		{
			if(event.param.errno != 0){
				trace('request error')
			}
			
			switch(event.param.rtype){
				case 'auth':{
					dispatch(new AuthRetEvent(
						AuthRetEvent.AUTH_RET,
						event.param.username,
						event.param.sid,
						event.param.errno==null?0:event.param.errno));
				}
			}
		}
		
	}
}