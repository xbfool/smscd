// ActionScript file



package com.xbfool.smsc.controller
{
	import flash.events.Event;
	import flash.events.TimerEvent;
	import flash.utils.Timer;
	
	import mx.controls.Alert;
	import mx.events.CloseEvent;
	import mx.managers.PopUpManager;
	
	public class SelfCloseAlert extends Event
	{
		private var alrt:Alert;
		private var alrtTimer:Timer;
		public function SelfCloseAlert(timeout:int = 5000):void {
			alrtTimer = new Timer(timeout, 1);
			alrtTimer.addEventListener(TimerEvent.TIMER_COMPLETE, removeAlert);
			super('SELFCLOSEALERT');
		}
		
		public function showAlert(text:String, title:String):void {
			alrt = Alert.show(text, title, Alert.OK, null, this.alrt_close);
			alrtTimer.reset();
			alrtTimer.start();
		}
		
		private function alrt_close(evt:CloseEvent):void {
			alrtTimer.stop();
		}
		
		private function removeAlert(evt:TimerEvent):void {
			PopUpManager.removePopUp(alrt);
		}
	}
}