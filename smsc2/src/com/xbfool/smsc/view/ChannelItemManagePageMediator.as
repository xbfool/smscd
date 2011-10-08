// ActionScript file
package com.xbfool.smsc.view
{
	import com.xbfool.smsc.command.*;
	import com.xbfool.smsc.controller.*;
	import com.xbfool.smsc.event.*;
	import com.xbfool.smsc.model.*;
	import com.xbfool.smsc.services.*;
	import com.xbfool.smsc.view.*;
	
	import org.robotlegs.mvcs.Mediator;
	
	public class ChannelItemManagePageMediator extends Mediator
	{
		[Inject]
		public var channelItemManagePage:ChannelItemManagePage;
		[Inject]
		public var channelItemAddPage:ChannelItemAddPage;
		[Inject]
		public var requestObj:IRequestService;
		
		public function ChannelItemManagePageMediator()
		{
		}
		
		override public function onRegister():void
		{
			// view listeners
			eventMap.mapListener(channelItemManagePage, ChannelItemPageEvent.CHANNEL_ITEM_ADD_PAGE, onAdd);
			eventMap.mapListener(channelItemAddPage, ChannelItemPageEvent.CHANNEL_ITEM_ADD_ITEM, onAddItem);
			eventMap.mapListener(channelItemManagePage, ChannelItemPageEvent.CHANNEL_ITEM_QUERY, onQuery);
		}
		
		private function onAdd(e:ChannelItemPageEvent):void
		{
			contextView.addChild(channelItemAddPage);
		}
		private function onQuery(e:ChannelItemPageEvent):void
		{
			dispatch(new ChannelItemEvent(ChannelItemEvent.CHANNEL_ITEM_QUERY));
		}
		private function onAddItem(e:ChannelItemPageEvent):void
		{
			dispatch(new ChannelItemEvent(ChannelItemEvent.CHANNEL_ITEM_ADD,
				channelItemAddPage.channel_name.text,
				channelItemAddPage.channel_desc.text,
				channelItemAddPage.channel_type.text));
				
		}
		
	}
}