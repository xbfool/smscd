// ActionScript file
// ActionScript file
package com.xbfool.smsc.view.message
{
	import com.xbfool.smsc.command.*;
	import com.xbfool.smsc.controller.*;
	import com.xbfool.smsc.event.*;
	import com.xbfool.smsc.model.*;
	import com.xbfool.smsc.services.*;
	import com.xbfool.smsc.utils.*;
	import com.xbfool.smsc.view.main.LoginPage;
	import com.xbfool.smsc.view.main.LoginPageEvent;
	import flash.events.*;
	import mx.events.*;
	import flash.net.FileReference;
	
	import mx.collections.ArrayCollection;
	import mx.controls.Alert;
	
	import org.robotlegs.mvcs.Mediator;

	public class MessageSendPageMediator extends Mediator
	{
		[Inject]
		public var messageSendPage:MessageSendPage;
		
		[Inject]
		public var requestObj:IRequestService;
		
		public var address_list:ArrayCollection = new ArrayCollection();
		public var address_file:FileReference = null;
		public var address_array:Array = new Array;
		public function MessageSendPageMediator()
		{
		}
		
		override public function onRegister():void
		{
			eventMap.mapListener(messageSendPage, MessageSendPageEvent.CLEAN, cleanMessageContent);
			eventMap.mapListener(messageSendPage, MessageSendPageEvent.MESSAGE_CHANGE, changeMessageStatus);
			eventMap.mapListener(messageSendPage, MessageSendPageEvent.ADD_ADDRESS, addAddress);
			eventMap.mapListener(messageSendPage, MessageSendPageEvent.ADDRESS_CHANGE, changeMessageStatus);
			eventMap.mapListener(messageSendPage, MessageSendPageEvent.FILTER_ADDRESS, filterAddress);
			eventMap.mapListener(messageSendPage, MessageSendPageEvent.DEL_ONE_ADDRESS, delOneAddress);
			eventMap.mapListener(messageSendPage, MessageSendPageEvent.CLEAN_ALL_ADDRESS, cleanAllAddress);
			eventMap.mapListener(messageSendPage, MessageSendPageEvent.IMPORT_ADDRESS_FILE, importAddressFile);
			eventMap.mapListener(messageSendPage, MessageSendPageEvent.SEND_MESSAGE, sendMessage);
			//eventMap.mapListener(messageSendPage, MessageSendPageEvent.SAVE_ADDRESS, saveAddress);
			messageSendPage.address_grid.dataProvider = address_list;
		}
		
		private function cleanMessageContent(e:MessageSendPageEvent):void {
			messageSendPage.message_content_text.text = "";
		
			messageSendPage.dispatchEvent(new MessageSendPageEvent(MessageSendPageEvent.MESSAGE_CHANGE));
		}
		
		private function changeMessageStatus(e:MessageSendPageEvent):void {
			var msgStatus:Object = MessageUtil.computeMessageNum(
				messageSendPage.message_content_text.text, address_list.length);
			messageSendPage.msgCharCount.text = msgStatus.msgCharCount;
			messageSendPage.msgSplitNum.text = msgStatus.splitNum;
			messageSendPage.addressNum.text = msgStatus.addressNum;
			messageSendPage.totalNum.text = msgStatus.totalNum;
			
		}
		
		private function addAddress(e:MessageSendPageEvent):void{
			var address:String = messageSendPage.new_address.text;
			if(MessageUtil.checkAddressValid(address)){
				address_list.addItem({number:messageSendPage.new_address.text});
				messageSendPage.new_address.text = "";
				messageSendPage.dispatchEvent(new MessageSendPageEvent(MessageSendPageEvent.ADDRESS_CHANGE));
			} else if(address.length != 0){
				Alert.show("不是有效的电话号码");	
			}
		}
		
		private function filterAddress(e:MessageSendPageEvent):void{
			var dp:Array = address_list.source;
			var dp1:Array = new Array;
			dp.sort();
			var o1:Object = null;
			var o2:Object = null;
			while(dp.length > 0) {
				o2 = dp.shift();
				if(o1 == null || o2.number != o1.number) {
					o1 = o2;
					dp1.push(o1);
				}		
			}
			address_list.source = dp1;
			messageSendPage.dispatchEvent(new MessageSendPageEvent(MessageSendPageEvent.ADDRESS_CHANGE));

		}
		
		private function cleanAllAddress(e:MessageSendPageEvent):void{
			address_list.source = new Array();
			messageSendPage.dispatchEvent(new MessageSendPageEvent(MessageSendPageEvent.ADDRESS_CHANGE));
		}
		
		private function delOneAddress(e:MessageSendPageEvent):void{
			//TODO
		}
		
		private function importAddressFile(e:MessageSendPageEvent):void{
			address_file = new FileReference();
			address_file.browse();
			
			address_file.addEventListener(Event.SELECT, selectHandler);
			address_file.addEventListener(Event.COMPLETE, completeHandler);
		}
		
		private function completeHandler(event:Event):void
		{
			var adds:String = address_file.data.toString();
			address_array = adds.match(/1[3458]\d{9}/g);
			for each(var item:String in address_array){
				address_list.addItem({number:item})
			}

			address_array = null;
			address_file = null;
			messageSendPage.dispatchEvent(new MessageSendPageEvent(MessageSendPageEvent.ADDRESS_CHANGE));
		}
		
		private function selectHandler(event:Event):void
		{
			address_file.load();
		}

		private function sendMessage(e:MessageSendPageEvent):void {
				Alert.buttonWidth = 100;
				Alert.yesLabel = "是";
				Alert.noLabel = "取消";
				//Alert.show("确认发送？","发送消息",3,this,doSendMessage(e);
		}
		
		private function doSendMessage(event:CloseEvent):void {
			if (event.detail==Alert.YES){
				
			}
		}

	}
}