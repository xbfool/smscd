// ActionScript file
package com.xbfool.smsc.view.main
{
	import com.xbfool.smsc.command.*;
	import com.xbfool.smsc.controller.*;
	import com.xbfool.smsc.event.*;
	import com.xbfool.smsc.model.*;
	import com.xbfool.smsc.services.*;
	import com.xbfool.smsc.view.main.LoginPage;
	import com.xbfool.smsc.view.main.LoginPageEvent;
	
	import org.robotlegs.mvcs.Mediator;

	public class LoginPageMediator extends Mediator
	{
		[Inject]
		public var loginPage:LoginPage;
		
		[Inject]
		public var requestObj:IRequestService;
		
		public function LoginPageMediator()
		{
		}
		
		override public function onRegister():void
		{
			// view listeners
			eventMap.mapListener(loginPage, LoginPageEvent.LOGIN_SUBMITTED, onLoginSubmitted);
			// context listeners
			eventMap.mapListener(eventDispatcher, UserProxyEvent.USER_LOGGED_IN, whenUserLoggedIn);
		}
		
		private function onLoginSubmitted(e:LoginPageEvent):void
		{
			eventDispatcher.dispatchEvent(
				new AuthReqEvent(AuthReqEvent.AUTH_REQ,
					loginPage.usernameTxt.text,
					loginPage.passwordTxt.text));
		}
		
		private function whenUserLoggedIn(e:UserProxyEvent):void
		{
			loginPage.closeAndRemove();
		}
		
	}
}