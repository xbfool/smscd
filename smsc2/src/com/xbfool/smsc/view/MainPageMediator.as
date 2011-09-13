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
		}
		
		private function whenUserLoggedOut(e:MainPageEvent):void 
		{
			eventDispatcher.dispatchEvent(
				new LogoutEvent(LogoutEvent.LOGOUT));
		}
			
	}
}