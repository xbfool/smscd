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
	
	public class ChannelListManagePageMediator extends Mediator
	{
		[Inject]
		public var channelListManagePage:ChannelListManagePage;
		[Inject]
		public var channelListAddPage:ChannelListAddPage;
		[Inject]
		public var requestObj:IRequestService;
		[Inject]
		public var user:UserProxy;
		public var channel_list_list:ArrayCollection = new ArrayCollection();
		public function ChannelListManagePageMediator()
		{
		}
		
		override public function onRegister():void
		{
			channelListManagePage.channel_list_grid.dataProvider = channel_list_list;
			// view listeners
			eventMap.mapListener(channelListManagePage, ChannelPageEvent.CHANNEL_LIST_ADD_PAGE, onAddPage);
			eventMap.mapListener(channelListAddPage, ChannelPageEvent.CHANNEL_LIST_ADD_ITEM, onAddItem);
			eventMap.mapListener(channelListManagePage, ChannelPageEvent.CHANNEL_LIST_DELETE, onDelete);
			eventMap.mapListener(channelListManagePage, ChannelPageEvent.CHANNEL_LIST_UPDATE, onUpdate);
			eventMap.mapListener(eventDispatcher, CompRetEvent.COMP_RET, onQueryBack);
			this.channelListAddPage.myDP.source = user.channel_item_list;
			this.channelListManagePage.myDP.source = user.channel_item_list;
			this.channel_list_list.source = user.channel_list_list;
		}
		
		private function onAddPage(e:ChannelPageEvent):void
		{
			contextView.addChild(channelListAddPage);
		}
		
		private function onAddItem(e:ChannelPageEvent):void
		{
			var req_list:Array = [{
				command:'channel_list_add',
				name:channelListAddPage.channel_name.text,
				desc:channelListAddPage.channel_desc.text,
				cm1:channelListAddPage.cm1.selectedItem.uid,
				cm2:channelListAddPage.cm2.selectedItem.uid,
				cm3:channelListAddPage.cm3.selectedItem.uid,
				cu1:channelListAddPage.cu1.selectedItem.uid,
				cu2:channelListAddPage.cu2.selectedItem.uid,
				cu3:channelListAddPage.cu3.selectedItem.uid,
				ct1:channelListAddPage.ct1.selectedItem.uid,
				ct2:channelListAddPage.ct2.selectedItem.uid,
				ct3:channelListAddPage.ct3.selectedItem.uid
			},
				{command:'channel_list_query_all'}];
			dispatch(new CompReqEvent(CompReqEvent.CompReq, req_list));
		}

		private function onQueryBack(e:CompRetEvent):void
		{
			this.channelListAddPage.myDP.source = user.channel_item_list;
			this.channelListManagePage.myDP.source = user.channel_item_list;
			this.channel_list_list.source = user.channel_list_list;
		}
		
		private function onUpdate(e:ChannelPageEvent):void
		{
			var req_list:Array = [{
				command:'channel_list_update',
				uid:channelListManagePage.channel_uid.text,
				values:{
				name:channelListManagePage.channel_name.text,
				desc:channelListManagePage.channel_desc.text,
				cm1:channelListManagePage.cm1.selectedItem.uid,
				cm2:channelListManagePage.cm2.selectedItem.uid,
				cm3:channelListManagePage.cm3.selectedItem.uid,
				cu1:channelListManagePage.cu1.selectedItem.uid,
				cu2:channelListManagePage.cu2.selectedItem.uid,
				cu3:channelListManagePage.cu3.selectedItem.uid,
				ct1:channelListManagePage.ct1.selectedItem.uid,
				ct2:channelListManagePage.ct2.selectedItem.uid,
				ct3:channelListManagePage.ct3.selectedItem.uid
				}
			},
				{command:'channel_list_query_all'}];
			dispatch(new CompReqEvent(CompReqEvent.CompReq, req_list));
		}
		
		private function onDelete(e:ChannelPageEvent):void
		{
			var req_list:Array = [{
				command:'channel_list_del',
				uid:channelListManagePage.channel_uid.text},
				{command:'channel_list_query_all'}];
			dispatch(new CompReqEvent(CompReqEvent.CompReq, req_list));
		}
	}
}