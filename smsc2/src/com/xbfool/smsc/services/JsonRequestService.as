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
	import flash.net.*;
	
	import mx.controls.Alert;
	
	import org.robotlegs.mvcs.Actor;
	public class JsonRequestService extends Actor implements IRequestService
	{
		[Inject]
		public var userProxy:UserProxy;
		public var is_requesting:Boolean = false;
		public function JsonRequestService()
		{
		}
		
		public function request(param:Object, sub_path = ""):void
		{	
			if(this.is_requesting)
				return
			var loader:URLLoader = new URLLoader;
			loader.dataFormat = URLLoaderDataFormat.TEXT;
			loader.addEventListener(Event.COMPLETE, data_arrive);
			loader.addEventListener(IOErrorEvent.IO_ERROR, io_error);
			
			var req:URLRequest = new URLRequest(userProxy.smsd_url + sub_path);
			
			req.method = URLRequestMethod.POST;
			req.contentType = 'application/json';
			req.data = JSON.encode(param);
			
			loader.load(req);
			this.is_requesting = true
		}
		
		private function data_arrive(evt:Event):void
		{
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
			var rtype:String = data['rtype'];
			if(rtype == null){
				trace('no rtype');
			}
			
			if(!RequestEvent.CheckType(data.rtype)){
				trace('invalid rtype: \'' + data.rtype + '\'');
			}	
			
			dispatch(new RetEvent(RetEvent.RET, data));
		}
		
		private function io_error(evt:Event):void
		{
			this.is_requesting = false;
			Alert.show("连接服务器失败,请检查网络连接");
			trace('io error');
		}

	}
}