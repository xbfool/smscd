// ActionScript file
package com.xbfool.smsc.view
{
	import com.xbfool.smsc.command.*;
	import com.xbfool.smsc.controller.*;
	import com.xbfool.smsc.event.*;
	import com.xbfool.smsc.model.*;
	import com.xbfool.smsc.services.*;
	import com.xbfool.smsc.view.*;
	
	import org.robotlegs.mvcs.Mediator;
	
	public class MainPageMediator extends Mediator
	{
		[Inject] public var mainPage:MainPage;
		[Inject] public var changePasswordPage:ChangePasswordPage;
		[Inject] public var channelLogPage:ChannelLogPage;
		[Inject] public var manageAddressPage:ManageAddressPage;
		[Inject] public var manageUserPage:ManageUserPage;
		[Inject] public var messageChartPage:MessageChartPage;
		[Inject] public var moneyLogPage:MoneyLogPage;
		[Inject] public var messageSendPage:MessageSendPage;
		[Inject] public var messageLogPage:MessageLogPage;
		[Inject] public var specialSendPage:SpecialSendPage;
		[Inject] public var uploadMessagePage:UploadMessagePage;
		[Inject] public var requestObj:IRequestService;
		
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
			mainPage.content_panel.addElement(messageSendPage);
		}
		
		private function changeToSpecialSendView(e:MainPageEvent):void
		{
			clearCurrentView();
			mainPage.content_panel.addElement(specialSendPage);
			
		}
		
		private function changeToMessageLogView(e:MainPageEvent):void
		{
			clearCurrentView();
			mainPage.content_panel.addElement(messageLogPage);
		}
		
		private function changeToMessageChartView(e:MainPageEvent):void
		{
			clearCurrentView();
			mainPage.content_panel.addElement(messageChartPage);
		}
		
		private function changeToMoneyLogView(e:MainPageEvent):void
		{
			clearCurrentView();
			mainPage.content_panel.addElement(moneyLogPage);
		}
		
		private function changeToManageAddressView(e:MainPageEvent):void
		{
			clearCurrentView();
			mainPage.content_panel.addElement(manageAddressPage);
		}
			
		private function changeToUploadMessageView(e:MainPageEvent):void
		{
			clearCurrentView();
			mainPage.content_panel.addElement(uploadMessagePage);
		}
		
		private function changeToChannelLogView(e:MainPageEvent):void
		{
			clearCurrentView();
			mainPage.content_panel.addElement(channelLogPage);
		}
		
		private function changeToManageUserView(e:MainPageEvent):void
		{
			clearCurrentView();
			mainPage.content_panel.addElement(manageUserPage);
		}
		
		private function changeToChangePasswordView(e:MainPageEvent):void
		{
			clearCurrentView();
			mainPage.content_panel.addElement(changePasswordPage);
		}
	}
}