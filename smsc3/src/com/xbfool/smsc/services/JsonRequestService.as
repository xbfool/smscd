package com.xbfool.smsc.services
{
	import com.adobe.crypto.SHA1;
	import com.adobe.serialization.json.JSON;
	import com.adobe.serialization.json.JSONParseError;
	import com.as3xls.xls.ExcelFile;
	import com.as3xls.xls.Sheet;
	import com.xbfool.smsc.controller.*;
	import com.xbfool.smsc.event.*;
	import com.xbfool.smsc.model.*;
	
	import flash.events.Event;
	import flash.events.IOErrorEvent;
	import flash.events.TimerEvent;
	import flash.net.*;
	import flash.utils.Timer;
	
	import mx.controls.Alert;
	import mx.events.CloseEvent;
	import mx.managers.PopUpManager;
	
	import org.robotlegs.mvcs.Actor;
	public class JsonRequestService extends Actor implements IRequestService
	{
		[Inject]
		public var userProxy:UserProxy;
		public var is_requesting:Boolean = false;
		private var alrt:Alert;
		private var alrtTimer:Timer;
		private var selfCloseAlert:SelfCloseAlert = new SelfCloseAlert(2000)
		public function JsonRequestService()
		{
		}
		
		public function request(param:Object, sub_path:String = ""):void
		{	
			if(this.is_requesting)
				return
			dispatch(new ProcessingEvent(ProcessingEvent.PROCESSING_BEGIN));
			var loader:URLLoader = new URLLoader;
			loader.dataFormat = URLLoaderDataFormat.TEXT;
			loader.addEventListener(Event.COMPLETE, data_arrive);
			loader.addEventListener(IOErrorEvent.IO_ERROR, io_error);
			
			var req:URLRequest = new URLRequest(userProxy.smsd_url + sub_path);
			
			req.method = URLRequestMethod.POST;
			req.contentType = 'application/json';
			req.data = JSON.encode(param);
			trace(req.data)
			this.is_requesting = true;
			
			loader.load(req);

		}
		
		private function data_arrive(evt:Event):void
		{
			dispatch(new ProcessingEvent(ProcessingEvent.PROCESSING_END));
			this.is_requesting = false;
			var l:URLLoader = evt.target as URLLoader;
			var raw_data:String = l.data as String;
			var data:Object = null;

			try{
				data = JSON.decode(raw_data);
			}
			catch(err:JSONParseError){
				trace('JSONParseError');
			}
			
			if(data == null){
				trace('json parser returns nothing');
			}
			var command:String = data['command'];
			if(command == null){
				trace('no command');
			}
			
			if(!RequestEvent.CheckType(data.command)){
				trace('invalid command: \'' + data.command + '\'');
			}	
			
			dispatch(new RetEvent(RetEvent.RET, data));
		}
		
		private function io_error(evt:Event):void
		{
			dispatch(new ProcessingEvent(ProcessingEvent.PROCESSING_END));
			this.is_requesting = false;
			this.selfCloseAlert.showAlert("连接服务器失败,请检查网络连接", "错误");
			trace('io error');
		}
		

	}
}