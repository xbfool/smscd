// ActionScript file
package com.xbfool.smsc.view
{
	import com.xbfool.smsc.command.*;
	import com.xbfool.smsc.controller.*;
	import com.xbfool.smsc.event.*;
	import com.xbfool.smsc.model.*;
	import com.xbfool.smsc.services.*;
	import com.xbfool.smsc.view.LoginPage;
	import com.xbfool.smsc.view.LoginPageEvent;
	
	import org.robotlegs.mvcs.Mediator;
	
	public class MainPageMediator extends Mediator
	{
		[Inject]
		public var mainPage:MainPage;
		
		[Inject]
		public var requestObj:IRequestService;
		
		public function MainPageMediator()
		{
		}
		
		override public function onRegister():void
		{
			eventMap.mapListener(mainPage, MainPageEvent.LOGOUT, whenUserLoggedOut);
			eventMap.mapListener(mainPage, MainPageEvent.MESSAGE_SEND_VIEW, changeToMessageSendView);
			eventMap.mapListener(mainPage, MainPageEvent.SPECIAL_SEND_VIEW, changeToSpecialSendView);
			eventMap.mapListener(mainPage, MainPageEvent.MESSAGE_LOG_VIEW, changeToMessageLogView);
			eventMap.mapListener(mainPage, MainPageEvent.MESSAGE_CHART_VIEW, changeToMessageChartView);
			eventMap.mapListener(mainPage, MainPageEvent.MONEY_LOG_VIEW, changeToMoneyLogView);
			eventMap.mapListener(mainPage, MainPageEvent.MANAGE_ADDRESS_VIEW, changeToManageAddressView);
			eventMap.mapListener(mainPage, MainPageEvent.UPLOAD_MESSAGE_VIEW, changeToUploadMessageView);
			eventMap.mapListener(mainPage, MainPageEvent.CHANNEL_LOG_VIEW, changeToChannelLogView);
			eventMap.mapListener(mainPage, MainPageEvent.MANAGE_USER_VIEW, changeToManageUserView);
			eventMap.mapListener(mainPage, MainPageEvent.CHANGE_PASSWORD_VIEW, changeToChangePasswordView);
		}
		
		private function whenUserLoggedOut(e:MainPageEvent):void 
		{
			eventDispatcher.dispatchEvent(
				new LogoutEvent(LogoutEvent.LOGOUT));
		}
		
		private function clearCurrentView():void 
		{
			mainPage.content_panel.removeAllElements();
		}
		
		private function changeToMessageSendView(e:MainPageEvent):void
		{
			clearCurrentView();
			mainPage.content_panel.addElement(new SendMessagePage());
		}
		
		private function changeToSpecialSendView(e:MainPageEvent):void
		{
			clearCurrentView();
		}
		
		private function changeToMessageLogView(e:MainPageEvent):void
		{
			clearCurrentView();
		}
		
		private function changeToMessageChartView(e:MainPageEvent):void
		{
			clearCurrentView();
		}
		
		private function changeToMoneyLogView(e:MainPageEvent):void
		{
			clearCurrentView();
		}
		
		private function changeToManageAddressView(e:MainPageEvent):void
		{
			clearCurrentView();
		}
			
		private function changeToUploadMessageView(e:MainPageEvent):void
		{
			clearCurrentView();
		}
		
		private function changeToChannelLogView(e:MainPageEvent):void
		{
			clearCurrentView();
		}
		
		private function changeToManageUserView(e:MainPageEvent):void
		{
			clearCurrentView();
		}
		
		private function changeToChangePasswordView(e:MainPageEvent):void
		{
			clearCurrentView();
		}
	}
}