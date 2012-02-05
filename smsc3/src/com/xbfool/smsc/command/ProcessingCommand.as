// ActionScript file
package com.xbfool.smsc.command
{
	import com.xbfool.smsc.controller.*;
	import com.xbfool.smsc.model.*;
	import com.xbfool.smsc.view.main.*;
	import org.robotlegs.mvcs.Command;
	public class ProcessingCommand extends Command
	{	
		[Inject]
		public var userProxy:UserProxy;
		[Inject]
		public var processingBarPage: ProcessingBarPage;
		
		override public function execute():void
		{
			contextView.addChild(processingBarPage);
		}
	}
}