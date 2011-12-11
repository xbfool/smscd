// ActionScript file
package com.xbfool.smsc.view.card
{
	import com.xbfool.smsc.command.*;
	import com.xbfool.smsc.controller.*;
	import com.xbfool.smsc.event.*;
	import com.xbfool.smsc.model.*;
	import com.xbfool.smsc.services.*;
	import com.xbfool.smsc.view.*;
	
	import mx.collections.ArrayCollection;
	
	import org.robotlegs.mvcs.Mediator;
	
	public class CardItemPageMediator extends Mediator
	{
		//[Inject]
		//public var cardItemManagePage:CardItemManagePage;
		[Inject]
		public var cardItemAddPage:CardItemAddPage;
		[Inject]
		public var cardItemManagePage:CardItemManagePage;
		[Inject]
		public var requestObj:IRequestService;
		[Inject]
		public var user:UserProxy;
		public var card_item_list:ArrayCollection = new ArrayCollection();
		
		public function CardItemPageMediator()
		{
		}
		
		override public function onRegister():void
		{
			// view listeners
			cardItemManagePage.card_item_grid.dataProvider = card_item_list;
			eventMap.mapListener(cardItemManagePage, CardPageEvent.CARD_ITEM_ADD_PAGE, onAddPage);
			eventMap.mapListener(cardItemAddPage, CardPageEvent.CARD_ITEM_ADD_ITEM, onAddItem);
			eventMap.mapListener(cardItemManagePage, CardPageEvent.CARD_ITEM_DELETE, onDelete);
			eventMap.mapListener(cardItemManagePage, CardPageEvent.CARD_ITEM_UPDATE, onUpdate);
			eventMap.mapListener(cardItemManagePage, CardPageEvent.CARD_ITEM_QUERY, onQuery);
			eventMap.mapListener(eventDispatcher, CompRetEvent.COMP_RET, onQueryBack);
			card_item_list.source = user.channel_item_list;
		}
		
		private function onAddPage(e:CardPageEvent):void
		{
			contextView.addChild(cardItemAddPage);
		}
		
		private function onQuery(e:CardPageEvent):void
		{
			var req_list:Array = [
				{command:'card_item_query'}
			];
			dispatch(new CompReqEvent(CompReqEvent.CompReq, req_list));
		}
		
		private function onAddItem(e:CardPageEvent):void
		{
			var req_list:Array = [{
				command:'card_item_add',
				number:cardItemAddPage.number.text,
				type:cardItemAddPage.type.text,
				provider:cardItemAddPage.provider.text,
				due_time:cardItemAddPage.due_time.text,
				total_max:cardItemAddPage.total_max.text,
				month_max:cardItemAddPage.month_max.text,
				day_max:cardItemAddPage.day_max.text,
				hour_max:cardItemAddPage.hour_max.text,
				minute_max:cardItemAddPage.minute_max.text},
				{command:'card_item_query'}
				];
			dispatch(new CompReqEvent(CompReqEvent.CompReq, req_list));
		}
		
		private function onQueryBack(e:CompRetEvent):void
		{
			card_item_list.source = user.card_item_list;
		}
		
		private function onUpdate(e:CardPageEvent):void
		{
			var req_list:Array = [{
				command:'card_item_update',
				uid:cardItemManagePage.card_uid.text,
				type:cardItemManagePage.type.text,
				provider:cardItemManagePage.provider.text,
				due_time:cardItemManagePage.due_time.text,
				total_max:cardItemManagePage.total_max.text,
				month_max:cardItemManagePage.month_max.text,
				day_max:cardItemManagePage.day_max.text,
				hour_max:cardItemManagePage.hour_max.text,
				minute_max:cardItemManagePage.minute_max.text},
				{command:'card_item_query'}
			];
			dispatch(new CompReqEvent(CompReqEvent.CompReq, req_list));
		}
		
		
		private function onDelete(e:CardPageEvent):void
		{
			var req_list:Array = [{
				command:'card_item_delete', uid:cardItemManagePage.card_uid.text},
				{command:'card_item_query'}
			];
			dispatch(new CompReqEvent(CompReqEvent.CompReq, req_list));
		}
		
	}
}