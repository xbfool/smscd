// ActionScript file
package com.xbfool.smsc.model {
	
	import org.robotlegs.mvcs.Actor;
	public class UserProxy extends Actor {
		private var username:String;
		private var loggedIn:Boolean;
		
		public var sessionId:String;
		public var smsd_url:String;
		public var channel_item_list:Object;
		public function UserProxy() {
			smsd_url = 'http://localhost:8080/smsd';
			loggedIn = false;
			username = '';
			sessionId = '';
		}
		
		public function setUsername(username:String):void {
			this.username = username;
			dispatch(new UserProxyEvent(UserProxyEvent.USERNAME_CHANGED));
		}
		
		public function set userLoggedIn(value:Boolean):void {
			loggedIn = value;
			if (loggedIn) {
				dispatch(new UserProxyEvent(UserProxyEvent.USER_LOGGED_IN));
			}
			else {
				dispatch(new UserProxyEvent(UserProxyEvent.USER_LOGGED_OUT));
			}
		}
		
		public function get userLoggedIn():Boolean{
			return loggedIn;
		}
		
		public function LogOutAndClean():void{
			this.username = '';
			this.loggedIn = false;
			this.sessionId = '';
		}
		
	}
}