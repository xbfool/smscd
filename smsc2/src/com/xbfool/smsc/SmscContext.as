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
		public var mainPage:MainPage;
		public var processingBarPage:ProcessingBarPage;
		public function SmscContext() {
			super();
		}
		
		override public function startup():void {
			this.mainPage = new MainPage();
			this.processingBarPage = new ProcessingBarPage()
			this.init_command();
			this.init_injector();
			this.init_map_view();
			super.startup();
			
			contextView.addChild( this.mainPage);
			contextView.addChild(new LoginPage());
		}
		
		public function init_command():void{
			commandMap.mapEvent(RetEvent.RET, RetCommand, RetEvent);
			commandMap.mapEvent(AuthReqEvent.AUTH_REQ, AuthReqCommand, AuthReqEvent);
			commandMap.mapEvent(AuthRetEvent.AUTH_RET, AuthRetCommand, AuthRetEvent);
			commandMap.mapEvent(LogoutEvent.LOGOUT, LogoutCommand, LogoutEvent);
			commandMap.mapEvent(ChannelItemAddEvent.CHANNEL_ITEM_ADD, ChannelItemAddCommand, ChannelItemAddEvent);
			commandMap.mapEvent(ProcessingEvent.PROCESSING_BEGIN, ProcessingCommand, ProcessingEvent);
		}
		
		public function init_injector():void{
			injector.mapSingleton(UserProxy);
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
			injector.mapSingleton(ChannelItemManagePage);
			injector.mapSingleton(ChannelListManagePage);
			injector.mapSingleton(UserChannelManagePage);
			injector.mapSingleton(ChannelItemAddPage);
			injector.mapValue(ProcessingBarPage, this.processingBarPage);
			injector.mapValue(MainPage, this.mainPage);
		}
		
		public function init_map_view():void{
			mediatorMap.mapView(LoginPage, LoginPageMediator);
			mediatorMap.mapView(ChannelItemManagePage, ChannelItemManagePageMediator);
			mediatorMap.mapView(ChannelItemAddPage, ChannelItemManagePageMediator);
			mediatorMap.mapView(MainPage, MainPageMediator);
			mediatorMap.mapView(MessageSendPage, MessageSendPageMediator);
			mediatorMap.mapView(ProcessingBarPage, ProcessingBarPageMediator);
		}
	}
}