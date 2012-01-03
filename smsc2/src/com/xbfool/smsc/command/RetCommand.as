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
		
		private function add_index(l:Array):void{
			for(var i:int = 0; i < l.length; i++){
				var o:Object = l[i];
				o.index = i + 1;
			}
		}
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
							user.channel_item_list.sortOn(['name']);
							this.add_index(user.channel_item_list);
						}
						break;
					}
					case 'channel_list_query_all':{
						if(item.errno == 0){
							user.channel_list_list = item.ret;
							user.channel_list_list.sortOn(['name']);
							this.add_index(user.channel_list_list);
						}
						break;
					}
					case 'user_query_all':{
						if(item.errno == 0){
							user.user_channel_list = item.ret;
							user.user_channel_list.sortOn(['username']);
							this.add_index(user.user_channel_list);
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
							user.card_item_list.sortOn(['number']);
							this.add_index(user.card_item_list)
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