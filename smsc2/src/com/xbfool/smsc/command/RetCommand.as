// ActionScript file
// ActionScript file
// ActionScript file
package com.xbfool.smsc.command
{
	import com.adobe.crypto.SHA1;
	import com.xbfool.smsc.controller.*;
	import com.xbfool.smsc.event.*;
	import com.xbfool.smsc.services.*;
	
	import org.robotlegs.mvcs.Command;
	
	public class RetCommand extends Command
	{
		[Inject]
		public var event:RetEvent;
		[Inject]
		public var reqestService:IRequestService;
		
		override public function execute():void
		{
			if(event.param.errno != 0){
				trace('request error')
			}
			for each (var item:Object in event.param){
				switch(item.command){
					case 'user_login':{
						dispatch(new AuthRetEvent(
							AuthRetEvent.AUTH_RET,
							item.ret.user.username,
							item.sid,
							item.errno==null?0:item.errno));
						break;
					}
					case 'channel_item_add':{
						//TODO
						break;
					}
					case 'channel_item_query_all':{
						trace(event.param);
						dispatch(new ChannelItemEvent(ChannelItemEvent.CHANNEL_ITEM_QUERY_RET,
							"","","",item.errno, item.ret));
						break;
					}
				}
			}
		}
		
	}
}