// ActionScript file
package com.xbfool.smsc.services
{
	import flash.net.*;
	import flash.events.Event;
	import flash.events.IOErrorEvent;
	import com.xbfool.smsc.model.*;
	import org.robotlegs.mvcs.Actor;
	import com.xbfool.smsc.controller.*;
	public class DummyRequestService extends Actor implements IRequestService
	{
		[Inject]
		public var userProxy:UserProxy;
		
		public function DummyRequestService()
		{
		}
		
		public function request(param:Object):void
		{	
			dispatch(new RequestEvent(param.q, param));
		}
	}
}