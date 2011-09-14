// ActionScript file
// ActionScript file
package com.xbfool.smsc.view
{
	import com.xbfool.smsc.command.*;
	import com.xbfool.smsc.controller.*;
	import com.xbfool.smsc.event.*;
	import com.xbfool.smsc.model.*;
	import com.xbfool.smsc.services.*;
	import com.xbfool.smsc.utils.*;
	import com.xbfool.smsc.view.LoginPage;
	import com.xbfool.smsc.view.LoginPageEvent;
	
	import org.robotlegs.mvcs.Mediator;
	
	public class MessageSendPageMediator extends Mediator
	{
		[Inject]
		public var messageSendPage:MessageSendPage;
		
		[Inject]
		public var requestObj:IRequestService;
		
		public function MessageSendPageMediator()
		{
		}
		
		override public function onRegister():void
		{
			eventMap.mapListener(messageSendPage, MessageSendPageEvent.CLEAN, cleanMessageContent);
			eventMap.mapListener(messageSendPage, MessageSendPageEvent.MESSAGE_CHANGE, changeMessageStatus);
		}
		
		private function cleanMessageContent(e:MessageSendPageEvent):void {
			messageSendPage.message_content_text.text = "";
			messageSendPage.dispatchEvent(new MessageSendPageEvent(MessageSendPageEvent.MESSAGE_CHANGE));
		}
		
		private function changeMessageStatus(e:MessageSendPageEvent):void {
			var msgStatus:Object = MessageUtil.computeMessageNum(
				messageSendPage.message_content_text.text, 1);
			messageSendPage.msgCharCount.text = msgStatus.msgCharCount;
			messageSendPage.msgSplitNum.text = msgStatus.splitNum;
			messageSendPage.addressNum.text = msgStatus.addressNum;
			messageSendPage.totalNum.text = msgStatus.totalNum;
			
		}
	}
}