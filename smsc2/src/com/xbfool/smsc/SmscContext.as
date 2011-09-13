package com.xbfool.smsc {
	import com.xbfool.smsc.command.*;
	import com.xbfool.smsc.controller.*;
	import com.xbfool.smsc.event.*;
	import com.xbfool.smsc.model.*;
	import com.xbfool.smsc.services.*;
	import com.xbfool.smsc.view.*;
	
	import mx.logging.Log;
	
	import org.robotlegs.mvcs.Context;

	public class SmscContext extends Context {
		public function SmscContext() {
			super();
		}
		
		override public function startup():void {
			commandMap.mapEvent(AuthReqEvent.AUTH_REQ, AuthReqCommand, AuthReqEvent);
			commandMap.mapEvent(AuthRetEvent.AUTH_RET, AuthRetCommand, AuthRetEvent);
			commandMap.mapEvent(RetEvent.RET, RetCommand, RetEvent);
			injector.mapSingleton(UserProxy);
			//injector.mapSingletonOf(IRequestService, DummyRequestService);
			injector.mapSingletonOf(IRequestService, JsonRequestService);
			mediatorMap.mapView(LoginPage, LoginPageMediator);
			super.startup();
			
			contextView.addChild(new LoginPage());
		}
	}
}