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
			eventMap.mapListener(eventDispatcher, CompRetEvent.COMP_RET, onQueryBack);
			this.userChannelManagePage.myDP.source = user.channel_list_list;
			this.user_list.source = user.user_channel_list;

		}
		
		private function onQueryBack(e:CompRetEvent):void
		{
			user_list.source = user.user_channel_list;
		}
		
		private function onUpdate(e:ChannelPageEvent):void
		{
			var req_list:Array = [{
				command:'user_update_channel_list',
				user_id:userChannelManagePage.user_grid.selectedItem.uid,
				channel_list_id:userChannelManagePage.channel_list_id.selectedItem.uid},
				{command:'user_query_all'}];
			dispatch(new CompReqEvent(CompReqEvent.CompReq, req_list));
		}
		
	}
}