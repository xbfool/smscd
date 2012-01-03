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
	
	import mx.controls.Alert;
	
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
					case 'user_query_all':{
						if(item.errno == 0){
							user.user_channel_list = item.ret;
						}
						break;
					}
					case 'card_item_query':{
						if(item.errno == 0){
							user.card_item_list = item.ret;
							for(var i:int = 0; i < user.card_item_list.length; i++){
								var o:Object = user.card_item_list[i];
								o.total_remain = o.total_max - o.total;
								o.month_remain = o.month_max - o.month;
								o.day_remain = o.day_max - o.day;
								o.hour_remain = o.hour_max - o.hour;
							}
						}
						break;
					}
					
					default:{
						if(item.errno != 0) {
							Alert.show(item.command +':failed, ' + item.errtext);
						}else{
							Alert.show('提交请求成功');
						}
					}
				}
				

			}
			dispatch(new CompRetEvent(CompRetEvent.COMP_RET));
		}
		
	}
}