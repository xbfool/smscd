// ActionScript file
package com.xbfool.smsc.view.card
{
	import com.xbfool.smsc.command.*;
	import com.xbfool.smsc.controller.*;
	import com.xbfool.smsc.event.*;
	import com.xbfool.smsc.model.*;
	import com.xbfool.smsc.services.*;
	import com.xbfool.smsc.view.*;
	
	import flash.events.Event;
	import flash.net.FileReference;
	import flash.utils.ByteArray;
	
	import mx.collections.ArrayCollection;
	import mx.controls.Alert;
	
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
		public var file:FileReference = null;
		public var data:Array = null;
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
			eventMap.mapListener(cardItemManagePage, CardPageEvent.CARD_ITEM_ADD_LIST, onAddList);
			eventMap.mapListener(cardItemManagePage, CardPageEvent.CARD_ITEM_DOWNLOAD_TEMPLATE, onDownloadTemplate);
			eventMap.mapListener(cardItemManagePage, CardPageEvent.CARD_ITEM_ADD_LIST_COMMIT, onCommitList);
			eventMap.mapListener(eventDispatcher, CompRetEvent.COMP_RET, onQueryBack);
			card_item_list.source = user.card_item_list;
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
		
		private function onAddList(e:CardPageEvent):void
		{
			data = null;
			file = new FileReference();
			file.browse();
			
			file.addEventListener(Event.SELECT, selectFile);
			file.addEventListener(Event.COMPLETE, completeFile);
		}
		
		private function selectFile(e:Event):void{
			file.load()
		}
		
		private function onDownloadTemplate(e:Event):void{
			var file:ByteArray = new ByteArray;
			file.writeMultiByte("手机号,类型,运营商,过期时间,最大总数,每月最大,每天最大,每小时最大,每分钟最大\r\n", "gb2312");
			file.writeMultiByte("18612345678,月卡,联通,20120101,10000,1000,100,10,1\r\n", "gb2312");
			var fr:FileReference = new FileReference();  
			fr.save(file,"卡发模版.csv"); 
		}
		
		private function isValid(value:String):Boolean
		{
			var result:String = value.match(/[0-9]*/)[0];
			
			return value.length == result.length;
		}
		
		private function dateIsValid(value:String):Boolean
		{
			var result:String = value.match(/201[0-9][0-1][0-9][0-3][0-9]/)[0];
			
			return value.length == result.length;
		}
		
		private function oneItem(s:String):Object{
			var col:Array = s.split(",");
			if(col.length != 9)
				return null;
			if(col[0].length != 11 || !isValid(col[0]))
				return null;
			if(! dateIsValid(col[3]))
				return null;
			if(! (isValid(col[4]) && isValid(col[5]) && isValid(col[6]) && isValid(col[7]) && isValid(col[8])))
				return null;
			
			var o:Object = {
				number:col[0],
				type:col[1],
				provider:col[2],
				due_time:col[3],
				total_max:col[4],
				month_max:col[5],
				day_max:col[6],
				hour_max:col[7],
				minute_max:col[8]
			}
			return o;
		}
		
		private function completeFile(e:Event):void{
			var adds:ByteArray = file.data;
			var contents:String = adds.readMultiByte(adds.length, "gb2312");
			var rows:Array = contents.split("\r\n");
			
			
			data = new Array;

			
			for ( var i:int = 1; i < rows.length; i++) {
				var row:String = rows[i];

				var o:Object = oneItem(row)
				if(o != null)
					data.push(o);	
			}
			var msg:String = '共导入' + data.length +'条数据，是否提交？';
			Alert.show(msg, '提交',3,cardItemManagePage, onCommitList);
		}
		
		private function onCommitList(e:Event):void{
			if(data == null)
				return;
			
			var req_list:Array = [{
				command:'card_item_add_list',
				list:data},
				{command:'card_item_query'}
			];
			dispatch(new CompReqEvent(CompReqEvent.CompReq, req_list));
		}
	}
}