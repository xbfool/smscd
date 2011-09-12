// ActionScript file
package com.xbfool.smsc.view
{
	import com.xbfool.smsc.model.UserProxyEvent;
	import com.xbfool.smsc.view.LoginPage;
	import com.xbfool.smsc.view.LoginPageEvent;
	import com.xbfool.smsc.controller.SystemEvent;
	import org.robotlegs.mvcs.Mediator;
	
	public class LoginPageMediator extends Mediator
	{
		[Inject]
		public var loginPage:LoginPage;
		
		//[Inject]
		//public var authService:IAuthService;
		
		public var triggerEvent:SystemEvent;
		
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
			//authService.login(loginPage.usernameTxt.text, loginPage.passwordTxt.text);
		}
		
		private function whenUserLoggedIn(e:UserProxyEvent):void
		{
			eventDispatcher.dispatchEvent(triggerEvent);
			loginPage.closeAndRemove();
		}
		
	}
}