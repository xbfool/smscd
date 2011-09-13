// ActionScript file
// ActionScript file
package com.xbfool.smsc.command
{
	import com.xbfool.smsc.controller.*;
	import com.xbfool.smsc.services.*;
	import com.xbfool.smsc.event.*;
	import org.robotlegs.mvcs.Command;
	import com.adobe.crypto.SHA1;
	
	public class AuthRetCommand extends Command
	{
		[Inject]
		public var event:AuthRetEvent;
		[Inject]
		public var reqestService:IRequestService;
		
		override public function execute():void
		{
			//TODO
			trace('auth ok');
		}
		
	}
}