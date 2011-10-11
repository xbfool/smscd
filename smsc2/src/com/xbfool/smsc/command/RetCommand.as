// ActionScript file
// ActionScript file
// ActionScript file
package com.xbfool.smsc.command
{
	import com.adobe.crypto.SHA1;
	import com.xbfool.smsc.controller.*;
	import com.xbfool.smsc.event.*;
	import com.xbfool.smsc.model.*;
	import com.xbfool.smsc.services.*;
	
	import org.robotlegs.mvcs.Command;
	
	public class RetCommand extends Command
	{
		[Inject]
		public var event:RetEvent;
		[Inject]
		public var reqestService:IRequestService;
		[Inject]
		public var user:UserProxy;
		override public function execute():void
		{
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
						break;
					}
					case 'channel_item_query_all':{
						if(item.errno == 0){
							user.channel_item_list = item.ret;
						}
						break;
					}
					case 'channel_list_query_all':{
						if(item.errno == 0){
							user.channel_list_list = item.ret;
						}
						break;
					}
				}
			}
			dispatch(new CompRetEvent(CompRetEvent.COMP_RET));
		}
		
	}
}