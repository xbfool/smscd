// ActionScript file
package com.xbfool.smsc.controller
{
	import com.xbfool.smsc.controller.*;
	import com.xbfool.smsc.model.*;
	import com.xbfool.smsc.view.*;
	import org.robotlegs.mvcs.Command;
	
	public class LogOut extends Command
	{
		[Inject]
		public var event:SystemEvent;
		
		[Inject]
		public var userProxy:UserProxy;
		
		
		override public function execute():void
		{
			userProxy.userLoggedIn = false;
			injector.mapValue(SystemEvent, event, 'LoginTrigger');
			contextView.addChild(new LoginPage());

		}
	}
}