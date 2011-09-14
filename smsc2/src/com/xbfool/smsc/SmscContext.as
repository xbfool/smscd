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
			commandMap.mapEvent(RetEvent.RET, RetCommand, RetEvent);
			commandMap.mapEvent(AuthReqEvent.AUTH_REQ, AuthReqCommand, AuthReqEvent);
			commandMap.mapEvent(AuthRetEvent.AUTH_RET, AuthRetCommand, AuthRetEvent);
			commandMap.mapEvent(LogoutEvent.LOGOUT, LogoutCommand, LogoutEvent);
			
			injector.mapSingleton(UserProxy);
			//injector.mapSingletonOf(IRequestService, DummyRequestService);
			injector.mapSingletonOf(IRequestService, JsonRequestService);
			injector.mapSingleton(ChangePasswordPage);
			injector.mapSingleton(ChannelLogPage);
			injector.mapSingleton(ManageAddressPage);
			injector.mapSingleton(ManageUserPage);
			injector.mapSingleton(MessageChartPage);
			injector.mapSingleton(MessageLogPage);
			injector.mapSingleton(MessageSendPage);
			injector.mapSingleton(MoneyLogPage);
			injector.mapSingleton(SpecialSendPage);
			injector.mapSingleton(UploadMessagePage);
			mediatorMap.mapView(LoginPage, LoginPageMediator);
			mediatorMap.mapView(MainPage, MainPageMediator);
			mediatorMap.mapView(MessageSendPage, MessageSendPageMediator);
			super.startup();
			
			contextView.addChild(new MainPage());
			contextView.addChild(new LoginPage());
		}
	}
}