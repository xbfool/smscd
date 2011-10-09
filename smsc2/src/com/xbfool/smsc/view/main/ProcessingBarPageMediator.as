package com.xbfool.smsc.view.main
{
	import org.robotlegs.mvcs.Mediator;
	import com.xbfool.smsc.view.*;
	import com.xbfool.smsc.event.*
	public class ProcessingBarPageMediator extends Mediator
	{
		[Inject]
		public var processingBarPage:ProcessingBarPage;
		
		public function ProcessingBarPageMediator()
		{
			super();
		}
		
		override public function onRegister():void
		{
			eventMap.mapListener(eventDispatcher, ProcessingEvent.PROCESSING_END, onClose);
		}
		
		private function onClose(e:ProcessingEvent):void{
			processingBarPage.closeAndRemove();
		}
		

	}
}