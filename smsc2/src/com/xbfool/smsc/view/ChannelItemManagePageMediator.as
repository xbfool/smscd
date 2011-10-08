// ActionScript file
package com.xbfool.smsc.view
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
		public var channel_item_list:ArrayCollection = new ArrayCollection();
		
		public function ChannelItemManagePageMediator()
		{
		}
		
		override public function onRegister():void
		{
			// view listeners
			eventMap.mapListener(channelItemManagePage, ChannelItemPageEvent.CHANNEL_ITEM_ADD_PAGE, onAdd);
			eventMap.mapListener(channelItemAddPage, ChannelItemPageEvent.CHANNEL_ITEM_ADD_ITEM, onAddItem);
			eventMap.mapListener(channelItemManagePage, ChannelItemPageEvent.CHANNEL_ITEM_QUERY, onQuery);
			eventMap.mapListener(eventDispatcher, ChannelItemEvent.CHANNEL_ITEM_QUERY_RET, onQueryBack);
			channelItemManagePage.channel_item_grid.dataProvider = channel_item_list;
		}
		
		private function onAdd(e:ChannelItemPageEvent):void
		{
			contextView.addChild(channelItemAddPage);
		}
		private function onQuery(e:ChannelItemPageEvent):void
		{
			dispatch(new ChannelItemEvent(ChannelItemEvent.CHANNEL_ITEM_QUERY_REQ));
		}
		private function onAddItem(e:ChannelItemPageEvent):void
		{
			if(	channelItemAddPage.channel_name.text != "" &&
				channelItemAddPage.channel_desc.text != "" &&
				channelItemAddPage.channel_type.text != ""){
				dispatch(new ChannelItemEvent(ChannelItemEvent.CHANNEL_ITEM_ADD,
					channelItemAddPage.channel_name.text,
					channelItemAddPage.channel_desc.text,
					channelItemAddPage.channel_type.text));
			} 
				
		}
		
		private function onQueryBack(e:ChannelItemEvent):void
		{
			var dp:Array = new Array;
			for each (var item:Object in e.query_ret_object){
				item.id = item.uid;
				dp.push(item);
			}
			channel_item_list.source = dp;
			

		}
		
	}
}