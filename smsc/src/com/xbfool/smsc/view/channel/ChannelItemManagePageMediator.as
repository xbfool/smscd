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
	
	public class ChannelItemManagePageMediator extends Mediator
	{
		[Inject]
		public var channelItemManagePage:ChannelItemManagePage;
		[Inject]
		public var channelItemAddPage:ChannelItemAddPage;
		[Inject]
		public var requestObj:IRequestService;
		[Inject]
		public var user:UserProxy;
		public var channel_item_list:ArrayCollection = new ArrayCollection();
		public const CHANNEL_START_TAG:int = 0;
		public const CHANNEL_STOP_TAG:int = 273;
		public function ChannelItemManagePageMediator()
		{
		}
		
		override public function onRegister():void
		{
			// view listeners
			channelItemManagePage.channel_item_grid.dataProvider = channel_item_list;
			
			eventMap.mapListener(channelItemManagePage, ChannelPageEvent.CHANNEL_ITEM_ADD_PAGE, onAddPage);
			eventMap.mapListener(channelItemAddPage, ChannelPageEvent.CHANNEL_ITEM_ADD_ITEM, onAddItem);
			eventMap.mapListener(channelItemManagePage, ChannelPageEvent.CHANNEL_ITEM_UPDATE, onUpdate);
			eventMap.mapListener(channelItemManagePage, ChannelPageEvent.CHANNEL_ITEM_DELETE, onDelete);
			eventMap.mapListener(channelItemManagePage, ChannelPageEvent.CHANNEL_ITEM_START, onStart);
			eventMap.mapListener(channelItemManagePage, ChannelPageEvent.CHANNEL_ITEM_STOP, onStop);
			eventMap.mapListener(eventDispatcher, CompRetEvent.COMP_RET, onQueryBack);
			channel_item_list.source = user.channel_item_list;
		}
		
		private function onAddPage(e:ChannelPageEvent):void
		{
			contextView.addChild(channelItemAddPage);
		}
		
		private function onQuery(e:ChannelPageEvent):void
		{
			dispatch(new ChannelItemEvent(ChannelItemEvent.CHANNEL_ITEM_QUERY_REQ));
		}
		
		private function onAddItem(e:ChannelPageEvent):void
		{
			var req_list:Array = [{
				command:'channel_item_add',
				name:channelItemAddPage.channel_name.text,
				desc:channelItemAddPage.channel_desc.text,
				type:channelItemAddPage.channel_type.text},
				{command:'channel_item_query_all'}];
			dispatch(new CompReqEvent(CompReqEvent.CompReq, req_list));
		}
		
		private function onQueryBack(e:CompRetEvent):void
		{
			channel_item_list.source = user.channel_item_list;
		}
		
		private function onUpdate(e:ChannelPageEvent):void
		{
			var req_list:Array = [{
				command:'channel_item_update',
				uid:channelItemManagePage.channel_uid.text,
				values:{
				name:channelItemManagePage.channel_name.text,
				desc:channelItemManagePage.channel_desc.text,
				type:channelItemManagePage.channel_type.text}},
				{command:'channel_item_query_all'}];
			dispatch(new CompReqEvent(CompReqEvent.CompReq, req_list));
		}
		
		private function onDelete(e:ChannelPageEvent):void
		{
			var req_list:Array = [{
				command:'channel_item_del',
				uid:channelItemManagePage.channel_uid.text},
				{command:'channel_item_query_all'}];
			dispatch(new CompReqEvent(CompReqEvent.CompReq, req_list));
		}
		
		private function onStart(e:ChannelPageEvent):void
		{
			var req_list:Array = [{
				command:'channel_item_update',
				uid:channelItemManagePage.channel_uid.text,
				values:{
					status:CHANNEL_START_TAG}},
				{command:'channel_item_query_all'}];
			dispatch(new CompReqEvent(CompReqEvent.CompReq, req_list));
		}
		
		private function onStop(e:ChannelPageEvent):void
		{
			var req_list:Array = [{
				command:'channel_item_update',
				uid:channelItemManagePage.channel_uid.text,
				values:{
					status:CHANNEL_STOP_TAG}},
				{command:'channel_item_query_all'}];
			dispatch(new CompReqEvent(CompReqEvent.CompReq, req_list));
		}
	}
}