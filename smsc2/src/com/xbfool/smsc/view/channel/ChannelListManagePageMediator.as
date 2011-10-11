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

		
		public function ChannelItemManagePageMediator()
		{
		}
		
		override public function onRegister():void
		{
			// view listeners
			eventMap.mapListener(channelListManagePage, ChannelPageEvent.CHANNEL_LIST_ADD_PAGE, onAddPage);
			eventMap.mapListener(channelListAddPage, ChannelPageEvent.CHANNEL_LIST_ADD_ITEM, onAddItem);
			eventMap.mapListener(channelListManagePage, ChannelPageEvent.CHANNEL_LIST_DELETE, onDelete);
			eventMap.mapListener(channelListManagePage, ChannelPageEvent.CHANNEL_LIST_UPDATE, onUpdate);
		}
		
		private function onAddPage(e:ChannelPageEvent):void
		{
			contextView.addChild(channelListAddPage);
		}
		
		private function onAddItem(e:ChannelPageEvent):void
		{
			
		}

		private function onUpdate(e:ChannelPageEvent):void
		{
			
		}
		
		private function onDelete(e:ChannelPageEvent):void
		{
			
		}
	}
}