package com.xbfool.smsc {
	import com.xbfool.smsc.controller.*;
	import com.xbfool.smsc.model.*;
	import com.xbfool.smsc.view.*;
	
	import mx.logging.Log;
	
	import org.robotlegs.mvcs.Context;

	public class SmscContext extends Context {
		public function SmscContext() {
			super();
		}
		
		override public function startup():void {
			commandMap.mapEvent(SystemEvent.LOG_OUT, LogOut);
			
			injector.mapSingleton(UserProxy);
			
			mediatorMap.mapView(LoginPage, LoginPageMediator);
			super.startup();
			
			contextView.addChild(new LoginPage());
		}
	}
}