// ActionScript file
//<![CDATA[
import com.adobe.crypto.SHA1;
import com.adobe.serialization.json.JSON;
import com.adobe.serialization.json.JSONParseError;

import flash.net.FileReference;
import mx.controls.Alert;
import mx.controls.Text;
import mx.controls.dataGridClasses.DataGridColumn;
import mx.events.CloseEvent;
import mx.events.ListEvent;
import mx.messaging.channels.StreamingAMFChannel;

public var smsd_url:String = 'http://localhost:8080/';
private var session:String;
private var address_file:FileReference = null;
private var address_file_text:String = '';
[Bindable] private var stage_id:int = 0; // 0 for login
//[Bindable] private var user_group:int = 1; //1 for admin, 2 for user
[Bindable] private var chart_data:Array;

//[Bindable] private var user_name: String = null;
[Bindable] private var grid_visible: Boolean = false;
//[Bindable] private var request_listmsg(user_name, 'all'):String;
[Bindable] private var login_prompt:String = '请输入用户名和密码';

//[Bindable] private var message_num_total: int = 0; 
//[Bindable] private var message_num_commited: int = 0; 
//[Bindable] private var message_num_remain: int = 0; 
//new
[Bindable] private var user_name: String = null; //username
[Bindable] private var user_msg_num:int = 0;//msg_num
[Bindable] private var user_flags:int = 0; //flags
[Bindable] private var user_create_time:String = null; //create_time
[Bindable] private var user_last_login:String =  null; //last_login

private function init():void {
	login_user.setFocus();
	if (this.parameters['smsd'] != null) {
		this.smsd_url = this.parameters['smsd'];
	}
	trace('smsd_url = ' + this.smsd_url);
}

private function request(param:Object):void {
	var loader:URLLoader = new URLLoader;
	loader.dataFormat = URLLoaderDataFormat.TEXT;
	loader.addEventListener(Event.COMPLETE, data_arrive);
	loader.addEventListener(IOErrorEvent.IO_ERROR, io_error);
	
	var req:URLRequest = new URLRequest(this.smsd_url);
	req.method = URLRequestMethod.POST;
	req.contentType = 'application/json';
	req.data = JSON.encode(param);
	
	loader.load(req);
}

private function data_arrive(evt:Event):void
{
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
	var processor:Function = this['processor_' + data.rtype];
	if(processor == null){
		trace('invalid rtype: \'' + data.rtype + '\'');
	}
	processor(data);
}

private function io_error(evt:Event):void
{
	Alert.show("连接服务器失败,请检查网络连接");
	trace('io error');
}

private function processor_auth(param:Object):void
{
	this.session = param.sid;
	this.user_name = param.username;
	
	trace('auth, sid = \'' + this.session + '\'');
//	change_stage(1);
	stage_id = 1;
	myViewStack.selectedChild = send_message_view;
	this.request({q:'userinfo', sid:this.session})
}

private function processor_userinfo(param:Object):void{
	this.user_name = param.user.username;
	this.user_msg_num = param.user.msg_num;
	this.user_flags = param.user.flags;
	this.user_create_time = param.user.create_time;
	this.user_last_login = param.user.last_login;
}

private const err_str:Array = [
	"",
	"登录失败",
	"登录超时",
	"服务器在处理请求时发生异常",
];

private function get_processor_name(str:String):String{
	switch(str){
		case 'auth':
			return "登录";
		case 'listuser':
			return "用户列表";
		case 'logout':
			return "注销";
		case 'changepwd':
			return "修改密码";
	}
	
	return "未知操作";
}
private function processor_err(param:Object):void
{
	Alert.show(err_str[param.errno]);
	if (param.errno == 2){
		// session expired, kick the client back to login
		//change_stage(0);
		stage_id = 0;
	}
}

private function login_chk(user:String, pass:String): Boolean {
	//trace('login_chk');
	if(user.length == 0){
		login_prompt = '请输入用户名';
		return false;
	}else if(pass.length == 0){
		login_prompt = '请输入密码';
		return false;
	}else{
		login_prompt = null;
		return true;
	}
}

private function login(user:String, pass:String):void {
	if(login_chk(user, pass)){
		this.request({q:'auth', user:user, pass:SHA1.hash(pass)});
	}
}

private function logout(): void {
	this.stage_id = 0;
	this.chart_data = null;
	
	///new
	this.user_name = null;
	this.user_msg_num = 0;
	this.user_flags = 0;
	this.user_create_time = null;
	this.user_last_login = null;
	
}

private function request_changepwd(old:String, newp1:String, newp2:String):void{
	if(newp1 != newp2){
		Alert.show("两次输入的密码不一致,请重新输入"); 
	}else if(newp1 == null && newp1 == ""){
		Alert.show("新密码不能为空,请重新输入");
	}else if(old == null && old == ""){
		Alert.show("旧密码不能为空,请重新输入");
	}
	else{
		
		this.request({q:'changepwd',sid:this.session, user:this.user_name, oldp:SHA1.hash(old), newp:SHA1.hash(newp1)});
	}
}

private function request_changepwd_admin(user:String, newp:String):void{
	this.request({q:'changepwd',sid:this.session, user:user, newp:SHA1.hash(newp)});
}

private function processor_changepwd(param:Object):void
{
	if(param.errno == 0)
		Alert.show("修改密码成功");
	else if(param.errno == 1)
		Alert.show("输入密码错误");
}

private function request_adduser(user:String, flags:int, pwd1:String, pwd2:String): void {
	//change_stage(1002);
	if(id == null && id == ""){
		Alert.show("用户名不能为空,请重新输入");
	}else if(pwd1 != pwd2){
		Alert.show("两次输入的密码不一致,请重新输入"); 
	}else if(pwd1 == null && pwd1 == ""){
		Alert.show("密码不能为空,请重新输入");
	}else{
		this.request({q:'adduser',sid:this.session,flags:flags,user:user, pass:SHA1.hash(pwd1)});		
	}
}

private function processor_adduser(param:Object):void{
	if(param.errno == 0){
		Alert.show("添加用户成功");
	}else if(param.errno == 1){
		Alert.show("不能添加重复用户");
	}
}

private function request_listchildren(): void {
	user_manage_viewstack.selectedChild = user_list_data_grid_view;
	this.request({q:'listchildren',sid:this.session});	
}

private function processor_listchildren(param:Object):void{
	if(param.errno != 0)
		Alert.show("遇到未知错误");
	else{
		
		var columns:Array = new Array;
		chart_data = new Array;
		var head:String = '序号,名字,剩余条数,创建时间, 上次登录时间, 角色';
		
		var head_cells:Array = head.split(',');
		for (var i:int = 0; i < head_cells.length; i++){
			var c:DataGridColumn = new DataGridColumn();
			c.dataField = 'c' + i.toString();
			c.dataTipField = c.dataField;
			c.headerText = head_cells[i];
			
			columns.push(c);
		}
		user_list_data_grid.columns = columns;
		
		var dp:Array = new Array;
		for (var j:int = 0;j < param.children.length; j++){
			var co:Object = param.children[j];
			var o:Object = new Object;
			o['c0'] = j + 1;
			o['c1'] = co.username;
			o['c2'] = co.msg_num;
			o['c3'] = co.create_time;
			o['c4'] = co.last_login;
			o['c5'] = display_role(co.flags);
			dp.push(o);
		}
		user_list_data_grid.dataProvider = dp;
		user_list_data_grid.doubleClickEnabled = true;
		user_list_data_grid.addEventListener(ListEvent.ITEM_DOUBLE_CLICK, user_list_grid_doubleclick_callback);
		
		

	}
}

private function request_addmessage(username:String, num: int):void{
	if(this.user_msg_num < num){
		Alert.show('余额不足');
	}else if(num <= 0){
		Alert.show('请输入数字');
	}else if(username == this.user_name){
		Alert.show('不能给自己充值');
	}
	else{
		this.request({q:'addmessage', sid:this.session, user:username, num:num});
	}
}

private function processor_addmessage(param:Object):void{
	this.user_msg_num -= param.num;
	this.managage_user_form_remain_message.text = 
		parseInt(this.managage_user_form_remain_message.text) + param.num;
	this.managage_user_form_add_message.text = null;
	Alert.show('充值成功');
}

private function request_sendmessage(action:String):void{
	if(action == 'normal'){
		var address:String = user_normal_phone_numbers.text;
		var message:String = user_normal_message_content.text;
		
		this.request({q:'sendmessage', sid:this.session, address:address, address_list:0, msg:message});
	}else if(action == 'file'){
		//todo
	}
}

private function processor_managemsg(param:Object):void{
	
	Alert.show('请求提交成功');
}

private function request_listmsg(user:String, status:int):void{
	this.request({q:'listmsg', sid:this.session, user:user, status:status});
}

private function msg_status_display(status:int):String{
	switch(status){
		case 1:
			return "提交";
		case 2:
			return "已发送";
		case 3:
			return "被拒绝";
		case 4:
			return "审批通过待发送";
	}
	
	return "未知状态";
}
private function processor_listmsg(param:Object):void{
	if(param.errno != 0)
		Alert.show("遇到未知错误");
	else{	
		var columns:Array = new Array;
		chart_data = new Array;
		var head:String = 'ID, 用户, 状态, 内容, 地址, 创建时间, 消息总数,上次修改时间';
		
		var head_cells:Array = head.split(',');
		for (var i:int = 0; i < head_cells.length; i++){
			var c:DataGridColumn = new DataGridColumn();
			c.dataField = 'c' + i.toString();
			c.dataTipField = c.dataField;
			c.headerText = head_cells[i];
			
			columns.push(c);
		}
		message_manage_data_grid.columns = columns;
		
		var dp:Array = new Array;
		for (var j:int = 0;j < param.msg.length; j++){
			var co:Object = param.msg[j];
			var o:Object = new Object;
			o['c0'] = co.uid;
			o['c1'] = co.username;
			o['c2'] = msg_status_display(co.status);
			o['c3'] = co.msg;
			o['c4'] = co.address;
			o['c5'] = co.create_time;
			o['c6'] = co.msg_num;
			o['c7'] = co.last_update;
			dp.push(o);
		}
		message_manage_data_grid.dataProvider = dp;
		message_manage_data_grid.doubleClickEnabled = true;
	
		message_manage_data_grid.addEventListener(ListEvent.ITEM_DOUBLE_CLICK, message_list_grid_doubleclick_callback);
	
	}
}

private function request_managemsg(uid:int, action:int):void{
	this.request({q:'managemsg', sid:this.session, uid:uid, action:action});
}

private function processor_sendmessage(param:Object):void{
	this.user_msg_num -= param.num;
	Alert.show('处理请求成功');
}


private function message_list_grid_doubleclick_callback(evt:Event):void{
	var event:mx.events.ListEvent = (mx.events.ListEvent)(evt);
	var index:int = event.rowIndex;
	var msg_entry:Object = message_manage_data_grid.dataProvider[index];
	
	managage_msg_view.visible = true;
	message_manage_data_grid.visible = false;
	managage_msg_form_id.text = msg_entry['c0'];
	managage_msg_form_name.text = msg_entry['c1'];
	managage_msg_form_status.text = msg_entry['c2'];
	managage_msg_form_addr.text = msg_entry['c4'];
	managage_msg_form_msg.text = msg_entry['c3'];
	managage_msg_form_create_time.text = msg_entry['c5'];
	managage_msg_form_num.text = msg_entry['c6'];
	managage_msg_form_last_update.text = msg_entry['c7'];
}

private function user_list_grid_doubleclick_callback(evt:Event):void{
	var event:mx.events.ListEvent = (mx.events.ListEvent)(evt);
	var index:int = event.rowIndex;
	var user_entry:Object = user_list_data_grid.dataProvider[index];
	
	managage_user_view.visible = true;
	user_list_data_grid.visible = false;
	managage_user_form_name.text = user_entry['c1'];
	mangage_user_form_role.text =  user_entry['c5'];
	mangage_user_form_create_time.text =user_entry['c3'];
	managage_user_form_remain_message.text = user_entry['c2']
	managage_user_form_last_login_time.text =  user_entry['c4'];
	managage_user_form_commit_times.text = (0 as int).toString();
}

private function get_user_log(date_from : Date, date_to :Date, action:String): void {

	this.request({q:'listlog', sid:this.session, 
		begin_year:date_from.fullYear, 
		begin_month:date_from.month + 1,
		begin_day:date_from.date,
		end_year:date_to.fullYear,
		end_month:date_to.month + 1,
		end_day:date_to.date,
		action:action});
}

private function processor_listlog(param:Object):void{
	
	var columns:Array = new Array;
	chart_data = new Array;
	var head:String = '序号,用户名,操作,操作时间,是否成功';
	
	var head_cells:Array = head.split(',');
	for (var i:int = 0; i < head_cells.length; i++){
		var c:DataGridColumn = new DataGridColumn();
		c.dataField = 'c' + i.toString();
		c.dataTipField = c.dataField;
		c.headerText = head_cells[i];
		
		columns.push(c);
	}
	user_log_data_grid.columns = columns;
	
	var dp:Array = new Array;
	for (var j:int = 0;j < param.l.length; j++){
		
		var o:Object = new Object;
		o['c0'] = j + 1;
		o['c1'] = param.l[j].username;
		o['c2'] = get_processor_name(param.l[j].query);
		o['c3'] = param.l[j].datetime;
		o['c4'] = param.l[j].errno == 0? '是':'否';
		dp.push(o);
	}
	user_log_data_grid.dataProvider = dp;
	user_log_data_grid.doubleClickEnabled = true;
	
}



private function user_send_file_message():void{
	user_normal_message_prompt.text = null;
	user_file_message_prompt.text = "请求已发送";
}

private function file_upload():void{
	address_file = new FileReference();
	address_file.browse()
	address_file.addEventListener(Event.SELECT, selectHandler);
	
}

private function selectHandler(event:Event):void
{
	try
	{
		file_name_label.text = address_file.name;
	}
	catch (error:Error)
	{
		trace("Unable to upload file.");
	}

}

private function check_char_count(text:TextArea, count:Label, address:String):void{
	var i:int = text.text.length;
	var p:int = (i - 1) / 70 + 1;
	var x:Array = address.split(';');
	var n:int = address.split(';').length;
	if(x[n-1] == '')
		n--;
	var num:int = p * n;
	count.text = "总字数:" + (i as int).toString() +" 总条数: " + (num as int).toString();
}


private function clear_content(text:TextArea):void{
	text.text = null;
}

private function clear_file():void{
	address_file = null;
	file_name_label.text = null;
}

private function display_role(flags:int):String{
	switch(flags){
		case 7:
			return "管理员";
		case 3:
			return "代理商";
		case 0:
			return "用户";
	}
	
	return "未知用户";
}
//		]]>