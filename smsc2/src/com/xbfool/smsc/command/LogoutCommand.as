// ActionScript file
package com.xbfool.smsc.command
{
	import com.xbfool.smsc.controller.*;
	import com.xbfool.smsc.model.*;
	import com.xbfool.smsc.view.*;
	import org.robotlegs.mvcs.Command;
	
	public class LogoutCommand extends Command
	{	
		[Inject]
		public var userProxy:UserProxy;
		
		
		override public function execute():void
		{
			userProxy.LogOutAndClean();
			contextView.addChild(new LoginPage());
		}
	}
}