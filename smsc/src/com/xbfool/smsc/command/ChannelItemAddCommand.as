// ActionScript file
package com.xbfool.smsc.command
{
	import com.xbfool.smsc.controller.*;
	import com.xbfool.smsc.services.*;
	import com.xbfool.smsc.event.*;
	import org.robotlegs.mvcs.Command;
	import com.adobe.crypto.SHA1;
	
	public class ChannelItemAddCommand extends Command
	{
		[Inject]
		public var event:ChannelItemEvent;
		[Inject]
		public var reqestService:IRequestService;
		
		override public function execute():void
		{
			reqestService.request({command:'channel_item_add', name:event.name, desc:event.desc, type:event.ctype});
		}
		
	}
}