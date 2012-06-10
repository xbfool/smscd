// ActionScript file
package com.xbfool.smsc.view.channel
{
	import com.xbfool.smsc.command.*;
	import com.xbfool.smsc.controller.*;
	import com.xbfool.smsc.event.*;
	import com.xbfool.smsc.model.*;
	import com.xbfool.smsc.services.*;
	import com.xbfool.smsc.view.*;
	
	import mx.collections.ArrayCollection;
	
	import org.robotlegs.mvcs.Mediator;
	
	public class UserChannelManagePageMediator extends Mediator
	{
		[Inject]
		public var userChannelManagePage:UserChannelManagePage;
		[Inject]
		public var requestObj:IRequestService;
		[Inject]
		public var user:UserProxy;
		public var user_list:ArrayCollection = new ArrayCollection();
		public function UserChannelManagePageMediator()
		{
		}
		
		override public function onRegister():void
		{
			userChannelManagePage.user_grid.dataProvider = user_list;
			// view listeners
			eventMap.mapListener(userChannelManagePage, ChannelPageEvent.USER_CHANNEL_LIST_UPDATE, onUpdate);
			eventMap.mapListener(userChannelManagePage, ChannelPageEvent.USER_CHANNEL_LIST_USE_NONE, onUseNone);
			eventMap.mapListener(eventDispatcher, CompRetEvent.COMP_RET, onQueryBack);
			this.userChannelManagePage.myDP.source = user.channel_list_list;
			this.userChannelManagePage.channelItemDP.source = user.channel_item_list;
			this.user_list.source = user.user_channel_list;

		}
		
		private function onQueryBack(e:CompRetEvent):void
		{
			user_list.source = user.user_channel_list;
		}
		
		private function onUpdate(e:ChannelPageEvent):void
		{
			var req_obj:Object = {
				command:'user_update_channel_list',
				user_id:userChannelManagePage.user_grid.selectedItem.uid,
				channe_cm:userChannelManagePage.channel_list_cm.selectedItem.name,
				channe_cu:userChannelManagePage.channel_list_cu.selectedItem.name,
				channe_ct:userChannelManagePage.channel_list_ct.selectedItem.name
			};
			
			if(userChannelManagePage.channel_list_id.selectedItem.uid >= 0){
				req_obj.channel_list_id = userChannelManagePage.channel_list_id.selectedItem.uid;
			}
			
			var req_list:Array = [req_obj]
				//{command:'user_query_all'}];
			dispatch(new CompReqEvent(CompReqEvent.CompReq, req_list));
		}
		
		private function onUseNone(e:ChannelPageEvent):void{
			var req_list:Array = [{
				command:'user_update_channel_list',
				user_id:userChannelManagePage.user_grid.selectedItem.uid,
				channel_list_id:-1},
				{command:'user_query_all'}];
			dispatch(new CompReqEvent(CompReqEvent.CompReq, req_list));
		}
	}
}