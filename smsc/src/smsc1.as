// ActionScript file

import com.adobe.crypto.SHA1;
import com.adobe.serialization.json.JSON;
import com.adobe.serialization.json.JSONParseError;
import com.as3xls.xls.ExcelFile;
import com.as3xls.xls.Sheet;

import flash.net.*;
import flash.net.FileReference;
import flash.utils.ByteArray;

import mx.collections.ArrayCollection;
import mx.collections.HierarchicalData;
import mx.controls.Alert;
import mx.controls.CheckBox;
import mx.controls.Text;
import mx.controls.dataGridClasses.DataGridColumn;
import mx.events.AdvancedDataGridEvent;
import mx.events.CloseEvent;
import mx.events.ListEvent;
import mx.messaging.AbstractConsumer;
import mx.messaging.channels.StreamingAMFChannel;

public var smsd_url:String = 'http://localhost:8082/';
//public var smsd_url:String = 'http://localhost/smsd/';
private var session:String;
private var selected_username:String = '';

[Bindable] private var stage_id:int = 0; // 0 for login
[Bindable] private var login_prompt:String = '请输入用户名和密码';

[Bindable] private var user_name: String = null; //username
[Bindable] private var user_msg_num:int = 0;//msg_num
[Bindable] private var user_flags:int = 0; //flags
[Bindable] private var user_create_time:String = null; //create_time
[Bindable] private var user_last_login:String =  null; //last_login
[Bindable] private var user_commit_msg_num:int = 0;

private var address_file:FileReference = new FileReference();
[Bindable]
public var message_type:ArrayCollection = new ArrayCollection(
	[ {label:"普通短信", data:1}, 
		{label:"促销短信", data:2}, 
		{label:"节日祝福", data:3},
		{label:"生日祝福", data:4},
		{label:"其他短信", data:5} ]);

[Bindable]
public var channel_select_data:ArrayCollection = new ArrayCollection(
	[ {label:"默认", data:'default'}, 
		{label:"电信0712a", data:'hb_ct_01'}, 
		{label:"电信0717a", data:'hb_ct_02'},
		{label:"电信0716a", data:'hb_ct_03'},
		{label:"电信10659a", data:'sd_ct_01'},
		{label:"三网106a", data:'hlyd_01'},
		{label:"联通106a", data:'changshang_a_01'},
		{label:"电信106a", data:'changshang_a_02'},
		{label:"移动106a", data:'changshang_a_03'},
		{label:"联通106ah", data:'changshang_a_04'},
		{label:"电信0728a", data:'hb_ct_04'},
	]);

[Bindable]
public var message_var_type:ArrayCollection = new ArrayCollection(
	[ {label:"请选择变量", data:0}, 
		{label:"姓名", data:1}, 
		{label:"节日祝福", data:2},
		{label:"手机号码", data:3},
		{label:"可选短信内容", data:4} ]);
[Bindable]
public var message_send_status:ArrayCollection = new ArrayCollection(
	[ {label:"全部", data:0}, 
		{label:"成功", data:2}, 
		{label:"失败", data:7},
	//	{label:"待审核", data:1},
		{label:"发送中", data:4},
	//	{label:"被拒绝", data:3}
	]);
[Bindable]
public var message_report_type:ArrayCollection = new ArrayCollection(
	[ {label:"短信发送统计表", data:0}, 
		{label:"每日发送流量统计表", data:1}, 
		{label:"号码段发送统计表", data:2},
		{label:"短信接收统计表", data:3} ]);


[Bindable]
private var select_username:String;
[Bindable]
private var select_userdesc:String;
[Bindable]
private var select_userrole:String;
[Bindable]
private var select_userpasswd:String;
[Bindable]
private var select_user_can_post:Boolean;
[Bindable]
private var select_user_can_weblogin:Boolean;
[Bindable]
private var select_user_need_check:Boolean;
[Bindable]
private var select_user_cm:int;
[Bindable]
private var select_user_cu:int;
[Bindable]
private var select_user_ct:int;
[Bindable]
private var self_user_cm:int;
[Bindable]
private var self_user_cu:int;
[Bindable]
private var self_user_ct:int;
[Bindable]
private var select_ext:String;
[Bindable]
private var user_data:ArrayCollection = new ArrayCollection();                                  
[Bindable]
private var check_mssage_list:ArrayCollection = new ArrayCollection();
[Bindable]
public var message_phone_number:ArrayCollection = new ArrayCollection();
[Bindable]
public var message_log_data:ArrayCollection = new ArrayCollection();
[Bindable]
public var addresslist_data:ArrayCollection = new ArrayCollection();

private function init():void {
	login_user.setFocus();
	if (this.parameters['smsd'] != null) {
		this.smsd_url = this.parameters['smsd'];
	}
	trace('smsd_url = ' + this.smsd_url);
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
	this.session = '';
	this.selected_username = '';
	
	this.stage_id = 0; // 0 for login
	this.login_prompt = '请输入用户名和密码';
	
	this.user_name = null; //username
	this.user_msg_num = 0;//msg_num
	this.user_flags = 0; //flags
	this.user_create_time = null; //create_time
	this.user_last_login =  null; //last_login
	this.user_commit_msg_num = 0;
	
	this.user_data = new ArrayCollection();                                  
	this.check_mssage_list = new ArrayCollection();
	this.message_phone_number = new ArrayCollection();
	this.addresslist_data = new ArrayCollection();
	this.login_pass.text = '';
//	user_grid.dataProvider = null;
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
	stage_id = 1;
	this.request({q:'userinfo', sid:this.session})
}

private function processor_userinfo(param:Object):void{
	this.user_name = param.user.username;
	this.user_msg_num = param.user.msg_num;
	this.user_flags = param.user.flags;
	this.user_create_time = param.user.create_time;
	this.user_last_login = param.user.last_login;
	this.user_commit_msg_num = param.user.commit_num;
	this.self_user_cm = get_channel_index(param.user.cm);
	this.self_user_cu = get_channel_index(param.user.cu);
	this.self_user_ct = get_channel_index(param.user.ct);
	channel_enable();
}

private function alert_not_impl():void{
	Alert.show("此功能暂时没有实现");
}

private const err_str:Array = [
	"",
	"登录失败",
	"您停留时间过长，请重新登陆。",
	"对不起,您无权对此操作。",
];


private function processor_err(param:Object):void
{
	Alert.show(err_str[param.errno]);
	if (param.errno == 2){
		// session expired, kick the client back to login
		//change_stage(0);
		stage_id = 0;
	}
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

private function processor_changepwd(param:Object):void
{
	if(param.errno == 0)
		Alert.show("修改密码成功");
	else if(param.errno == 1)
		Alert.show("输入密码错误");
}

private function request_adduser(user:String, name:String, pwd:String, can_weblogin:Boolean,
	can_post:Boolean, need_check:Boolean, cm:String, cu:String, ct:String): void {
	//change_stage(1002);
	if(id == null && id == ""){
		Alert.show("用户名不能为空,请重新输入");
	}else{
		var flags:int = 0;
		if(add_user_normal.selected)
			flags = 0;
		else if(add_user_agent.selected)
			flags = 3;
		else if(add_user_admin.selected)
			flags = 7;
		this.request({q:'adduser',sid:this.session,flags:flags,user:user, name:name, pass:SHA1.hash(pwd),
		can_weblogin:can_weblogin, can_post:can_post, need_check:need_check, cm:cm, cu:cu, ct:ct});		
	}
}

private function processor_adduser(param:Object):void{
	if(param.errno == 0){
		Alert.show("添加用户成功");
		request_listchildren();
	}else if(param.errno == 1){
		Alert.show("不能添加重复用户");
	}
}

private function request_listchildren(): void {
	//user_manage_viewstack.selectedChild = user_list_data_grid_view;
	this.request({q:'listchildren',sid:this.session});	
}

[Bindable] private var children_user_source:Array;
private function processor_listchildren(param:Object):void{
	if(param.errno != 0)
		Alert.show("遇到未知错误");
	else{
		var dp:Array = new Array;
		for (var j:int = 0;j < param.children.length; j++){
			var co:Object = param.children[j];
			var o:Object = new Object;
			dp.push(co);
		}
	//	user_data = dp;
		var hr:HierarchicalData = new HierarchicalData;
		hr.source = dp;
		children_user_source = dp;
		user_grid.dataProvider = hr;
		ViewStack_main.selectedChild = viewpage_user_manage;
	}
}


private function request_addmessage(username:String, num: int):void{
	if(user_grid == null || user_grid.selectedItem == null ||
		user_grid.selectedItem.username == '' || user_grid.selectedItem.username == null){
		Alert.show('请选择一个用户')
	}
	else{
		this.request({q:'addmessage', sid:this.session, user:user_grid.selectedItem.username, num:num});
	}
}

private function processor_addmessage(param:Object):void{
	if(param.errno == 0){
		request_listchildren();
		Alert.show('充值成功');
	}else if(param.errno == -1){
		Alert.show('余额不能小于0');
	}else if(param.errno == -2){
		Alert.show('充值数不能余额');
	}else if(param.errno == -3){
		Alert.show('不能给自己充值');
	}else if(param.errno == -4){
		Alert.show('不能给此用户充值');
	}
	message_add_input.text = "";
}

private function request_setuserstatus(status: int):void{
	
	if(user_grid.selectedItem == null || 
		user_grid.selectedItem.username == '' || 
		user_grid.selectedItem.username == null){
		Alert.show('请选择一个用户')
	}
	else{
		this.request({q:'setuserstatus', sid:this.session, user:user_grid.selectedItem.username, status:status});
	}
}

private function processor_setuserstatus(param:Object):void{
	if(param.errno == 0){
		request_listchildren();
		Alert.show('设置用户状态成功');
	}else if(param.errno == 1){
		Alert.show('不能禁用自己');
	}
}

private function request_manageuser(username:String, desc:String, pwd:String, role:String,
	can_weblogin:Boolean, can_post:Boolean, need_check:Boolean,cm:String,cu:String,ct:String, ext:String):void{
	var flags:int = 0;
	if(role == 'agent')
		flags = 3;
	else if(role == 'admin')
		flags = 7;
	
	if(this.user_name == username){
		if(flags != this.user_flags){
			Alert.show('不能改变自己的权限');
			return;
		}
	}
	
	
	if(pwd != null && pwd != ''){
		this.request({q:'manageuser', sid:this.session, user:username, desc:desc, pass:SHA1.hash(pwd), flags:flags,
		can_weblogin:can_weblogin, can_post:can_post, need_check:need_check, cm:cm, cu:cu, ct:ct, ext:ext});
	}else{
		this.request({q:'manageuser', sid:this.session, user:username, desc:desc, flags:flags,
		can_weblogin:can_weblogin, can_post:can_post, need_check:need_check, cm:cm, cu:cu, ct:ct, ext:ext});
	}
}

private function request_deleteuser():void{
	if(user_grid.selectedItem == null || 
		user_grid.selectedItem.username == '' || 
		user_grid.selectedItem.username == null){
		Alert.show('请选择一个用户');
	} else {
		var un:String = user_grid.selectedItem.username;
		this.request({q:'deleteuser', sid:this.session, user:un});
	}
}

private function processor_deleteuser(param:Object):void{
	if(param.errno == 0){
		request_listchildren();
		Alert.show('删除用户成功');
	}else if(param.errno == -1){
		Alert.show("不能删除有子用户的用户，请先删除子用户");
	}
	
}

private function get_channel_index(channel:String):int{
	switch(channel){
		case "default":
			return 0;
		case "hb_ct_01":
			return 1;
		case "hb_ct_02":
			return 2;
		case "hb_ct_03":
			return 3;
		case "sd_ct_01":
			return 4;
		case "hlyd_01":
			return 5;
		case "changshang_a_01":
			return 6;
		case "changshang_a_02":
			return 7;
		case "changshang_a_03":
			return 8;
		case "changshang_a_04":
			return 9;
		case "hb_ct_04":
			return 10;
		default:
			return 0;
	}
}
private function open_add_user_view():void{
	
	select_username = "";
	select_userdesc = "";
	select_userpasswd = "";
	ViewStack_main.selectedChild = viewpage_add_user;
	


}

private function open_managerview():void{
	if(user_grid.selectedItem == null || 
		user_grid.selectedItem.username == '' || 
		user_grid.selectedItem.username == null){
		Alert.show('请选择一个用户');
	}else{
		ViewStack_main.selectedChild = viewpage_manage_user;
		var user:Object = user_grid.selectedItem;
		//		var user:Object = 
		select_username = user.username;
		select_userdesc = user.description;
		if(user.flags == 3){
			select_userrole = 'agent';
		}else if(user.flags == 7){
			select_userrole = 'admin';
		}
		else{
			select_userrole = 'user';
		}
		select_user_can_weblogin = user.is_can_weblogin;
		select_user_can_post = user.is_can_post;
		select_user_need_check = user.is_need_check;
		select_user_cm = get_channel_index(user.cm);
		select_user_cu = get_channel_index(user.cu);
		select_user_ct = get_channel_index(user.ct);
		select_ext = user.ext;
		select_userpasswd = "";
		
		channel_enable();
		role_enable();

	}
}

private function open_msg_view():void{
	if(user_grid.selectedItem == null || 
		user_grid.selectedItem.username == '' || 
		user_grid.selectedItem.username == null){
		Alert.show('请选择一个用户');
	}else{
		ViewStack_main.selectedChild = viewpage_msg_manage;
		
	}
}

private function processor_manageuser(param:Object):void{
	if(param.errno == 0){
		Alert.show('修改用户信息成功');
		request_listchildren();
	} else if(param.errno == -2) {
		Alert.show('请在扩展号码中填入不多于5位的阿拉伯数字');
	}
	else
		Alert.show('您没有修改这些信息的权限');
}

private function addmessage_alertClickHandler(event:CloseEvent):void {
	if (event.detail==Alert.YES){
		var username:String = selected_username;
		var num:int = parseInt(message_add_input.text);
		request_addmessage(username, num);
	}
}

// Event handler function changes the default Button labels and sets the
// Button widths. If you later use an Alert with the default Buttons, 
// you must reset these values.
private function addmessage_alert(event:Event):void {
	Alert.buttonWidth = 100;
	Alert.yesLabel = "是";
	Alert.noLabel = "取消";
	Alert.show("确认充值？","充值",3,this,addmessage_alertClickHandler);
}

private var phone_address:Array;
private var phonename_list:Array;

private function is_phone_number(item:*, index:int, array:Array):Boolean{
	return item.type == PHONE_NUMBER;	
}

private function is_phone_name(item:*, index:int, array:Array):Boolean{
	return item.type == PHONE_NAME;	
}

private function sendmessage_alertClickHandler(event:CloseEvent):void {
	if (event.detail==Alert.YES){
		var dp:Array = message_phone_number.source;//.filter(is_selected);
		var phoneNumbers:Array = dp.filter(is_phone_number);
		var phoneNames:Array = dp.filter(is_phone_name);
		var address:Array = phoneNumbers.map(toAddress);
		this.phone_address = address.sort();
		var names:Array = phoneNames.map(toAddress);
		this.phonename_list = names.sort();
		conitune_sendmessage();
	}
}

private function conitune_sendmessage():void {
	if(this.phone_address != null && this.phone_address.length > 1000){
		var tmp_address:Array = this.phone_address.splice(0, 1000);
		var add_str:String = tmp_address.join(";");
		this.request({q:'sendmessage', sid:this.session, 
			address:add_str, address_list:0, msg:message_content_input.text, type:PHONE_NUMBER, remain:1});
	}
	else if ( this.phone_address != null && this.phone_address.length != 0 )
	{
		var add_str:String = this.phone_address.join(";");
		this.request({q:'sendmessage', sid:this.session, 
			address:add_str, address_list:0, msg:message_content_input.text, type:PHONE_NUMBER, remain:0});
		this.phone_address = null;
	}
	else {
		var add_str:String = this.phonename_list.join(";");
		this.request({q:'sendmessage', sid:this.session, 
			address:add_str, address_list:0, msg:message_content_input.text, type:PHONE_NAME, remain:0});
		this.phonename_list = null;
	}
}

private function get_address_str():String{
	var dp:Array = message_phone_number.source;//.filter(is_selected);
	var address:Array = dp.map(toAddress);
	var add_str:String = address.join(";");
	return add_str;
}

private function sendmessage_alert():void {
	Alert.buttonWidth = 100;
	Alert.yesLabel = "是";
	Alert.noLabel = "取消";
	Alert.show("确认发送？","发送消息",3,this,sendmessage_alertClickHandler);
}

private var PHONE_NUMBER:int = 1;
private var PHONE_NAME:int = 2;

private function add_phonenumber(number:String):void{
	if(number.length != 11 || number.charAt(0) != '1' 
		|| (number.charAt(1) != '3' &&
			number.charAt(1) != '4' &&
			number.charAt(1) != '5' &&
			number.charAt(1) != '8'
			))
			{
		Alert.show("不是有效的电话号码");	
	}
	else{
		message_phone_number.addItem({check:false, number:number, count:1, type:PHONE_NUMBER});
		message_new_number.text = "";
	}
	
	check_char_count(message_content_input, message_content_count, get_address_str());
}

private function erase_allphonenumber():void{
	message_phone_number.source = new Array();
	check_char_count(message_content_input, message_content_count, get_address_str());
}

private function is_not_selected(item:*, index:int, array:Array):Boolean{
	return item.check == false;	
}

private function delete_phonenumber():void{
	var newsource:Array = message_phone_number.source.filter(is_not_selected);
	message_phone_number.source = newsource;
	check_char_count(message_content_input, message_content_count, get_address_str());
}

private function import_phone_number_from_file():void{
	address_file = new FileReference();
	address_file.browse();
	
	address_file.addEventListener(Event.SELECT, selectHandler);
	address_file.addEventListener(Event.COMPLETE, completeHandler);
}

private function selectHandler(event:Event):void
{
	address_file.load();
}

private function completeHandler(event:Event):void
{
	var adds:String = address_file.data.toString();
	var adds_array:Array = adds.match(/1[3458]\d{9}/g);
	for(var i:int = 0; i < adds_array.length && i < 100000; i++){
		message_phone_number.addItem({check:false, number:adds_array[i], count:1, type:PHONE_NUMBER});
		if((i % 1000) == 0){
			check_char_count(message_content_input, message_content_count, get_address_str());
		}
	}
	check_char_count(message_content_input, message_content_count, get_address_str());
}
private function commit_message():void{
	var dp:Array = message_phone_number.source;//.filter(is_selected);
	if(dp.length == 0){
		Alert.show("请选择联系人");
	}else if(message_content_input.text.length == 0){
		Alert.show("请输入短信");
	}else if(dp.length >= 1000000){
		Alert.show("联系人数量超过上限(1000000个)，请删除一部分");
	}else if(dp.length + user_commit_msg_num > user_msg_num){
		Alert.show("余额不足");
	}else if(message_content_input.text.length > 500){
		Alert.show("短信字数超过上限(500字),请删除多余文字");
	}else{	
		sendmessage_alert();
	}
}

private function toAddress(element:*, index:int, arr:Array):String {
	return element.number;
}

private function processor_sendmessage(param:Object):void{
	if( (this.phone_address == null || this.phone_address.length == 0) 
		&& ( this.phonename_list == null || this.phonename_list.length == 0 )){
		this.request({q:'userinfo', sid:this.session});
		Alert.show('处理请求成功');
	}else{
		conitune_sendmessage();
	}
}

private function request_managemsg(status:String, isAll:Boolean):void{
	var dp:Array = check_mssage_list.source;
	var mlist:Array = new Array;
	
	var status_int:int = -1;
	if(isAll){
		for (var i:int = 0; i < dp.length; i++) {
			mlist.push(dp[i].uid)
		}
	}else{
		for (i = 0; i < dp.length; i++) {
			if(dp[i].check)
				mlist.push(dp[i].uid)
		}
	}
	if(status == "delete")
		status_int = 5;
	else if (status == "admit")
		status_int = 4;
	else if (status == "reject")
		status_int = 3;
	else if (status == "cancel")
		status_int = 6;

	if(mlist.length == 0){
		Alert.show("请至少选择一条信息");
	} else {
		this.request({q:'managemsg', sid:this.session, mlist:mlist, status: status_int});
	}
}

private function processor_managemsg(param:Object):void{
	Alert.show('请求提交成功');
	if(ViewStack_main.selectedChild == viewpage_message_send_log){
		request_listmsg(user_name,parseInt(message_send_log_status_select.value.toString()),
			message_send_log_date_from.selectedDate,
			message_send_log_date_to.selectedDate);
	} else {
		request_listcheckmsg();
	}
}

private function request_listcheckmsg():void{
	this.request({q:'listcheckmsg', sid:this.session});
}

private function processor_listcheckmsg(param:Object):void{
	if(param.errno != 0)
		Alert.show("遇到未知错误");
	else{
		var dp:Array = new Array;
		for (var j:int = 0;j < param.msg.length; j++){
			var co:Object = param.msg[j];
			co.check = false;
			dp.push(co);
		}
		check_mssage_list.source = dp;
	}
}

private function request_listmsg(user:String, status:int, begin:Date, end:Date):void{

	this.request({q:'listmsg', sid:this.session, user:user, status:status,
		begin:begin.time, end:end.time});
}

private function processor_listmsg(param:Object):void{
	if(param.errno != 0)
		Alert.show("遇到未知错误");
	else{	
		var dp:Array = new Array;
		for (var j:int = 0;j < param.msg.length; j++){
			var co:Object = param.msg[j];
			co.channel = channel_select_data[get_channel_index(co.channel)].label
			co.selected = 0;
			dp.push(co);
		}
		message_log_data.source = dp;

	}
}

private function delete_log_msg():void{
	var dp:Array = message_log_data.source;
	var mlist:Array = new Array;
	
	var status_int:int = 5; //delete

	for (var i:int = 0; i < dp.length; i++) {
		if(dp[i].selected)
			mlist.push(dp[i].uid)
	}

	status_int = 5;

	
	if(mlist.length == 0){
		Alert.show("请至少选择一条信息");
	} else {
		this.request({q:'managemsg', sid:this.session, mlist:mlist, status: status_int});
	}

}

private function deleteall_log_msg():void{
	var dp:Array = message_log_data.source;
	var mlist:Array = new Array;
	
	var status_int:int = 5; //delete
	
	for (var i:int = 0; i < dp.length; i++) {
		mlist.push(dp[i].uid)
	}
	
	status_int = 5;
	
	
	if(mlist.length == 0){
		Alert.show("没有信息可以删除");
	} else {
		this.request({q:'managemsg', sid:this.session, mlist:mlist, status: status_int});
	}
	
}

private function export_msg_log():void{

	var file:ByteArray = new ByteArray;
	var dataProviderCollection:ArrayCollection =  
		message_log_data as ArrayCollection; 
	var rowCount:int =  dataProviderCollection.length;
	file.writeUTFBytes("编号,发送人,发出时间,手机号码,通道,状态,条数,创建时间,短信内容\r\n");
	for(var r:int=0;r<rowCount;r++)  
	{  
		var record:Object =  
			dataProviderCollection.getItemAt(r);
		var status:String = msg_status_display(record.status);
		var ra:Array = new Array();
		ra.push(r.toString());
		ra.push(record.username);
		ra.push(record.last_update.toString());
		ra.push(record.address);
		ra.push(record.channel);
		ra.push(status);
		ra.push(record.msg_num.toString());
		ra.push(record.create_time.toString());
		ra.push(record.msg);
		ra.push("\r\n");
		ra.join(",");
		file.writeUTFBytes(ra.join(","));  
	}  
    var fr:FileReference = new FileReference();  
	
    fr.save(file,"msglog.txt");  
}

private function export_check_msg():void{
	
	var file:ByteArray = new ByteArray;
	var dataProviderCollection:ArrayCollection =  
		check_mssage_list as ArrayCollection; 
	var rowCount:int =  dataProviderCollection.length;
	file.writeUTFBytes("编号,发送人,提交时间,手机号码,号码总数,分割条数,短信内容\r\n");
	for(var r:int=0;r<rowCount;r++)  
	{  
		var record:Object =  
			dataProviderCollection.getItemAt(r);
		var status:String = msg_status_display(record.status);
		var ra:Array = new Array();
		ra.push(r.toString());
		ra.push(record.username);
		ra.push(record.create_time.toString());
		ra.push(record.address);
		ra.push(record.address.split(';').length.toString());
		ra.push(record.msg_num.toString());
		ra.push(record.msg.toString());
		ra.push("\r\n");
		ra.join(",");
		file.writeUTFBytes(ra.join(","));  
	}  
	var fr:FileReference = new FileReference();  
	
	fr.save(file,"msgcheck.txt");  
}

private function export_user():void{
	
	var file:ByteArray = new ByteArray;
	var dataProviderCollection:Array =  
		user_grid.dataProvider.source.source as Array; 
	var rowCount:int =  dataProviderCollection.length;
	file.writeUTFBytes("编号,ID,名称,账户状态,可用条数,允许web登录,允许接口发送,需要审核\r\n");
	var index:int = 1;
	for(var r:int=0;r<rowCount;r++) {  
		index = export_user_item(index,  dataProviderCollection[r], file);
	}  
	var fr:FileReference = new FileReference();
	
	fr.save(file,"exportuser.txt");  
}

private function export_user_item(index:int, record:Object, file:ByteArray):int{
	var status:String = msg_status_display(record.status);
	var ra:Array = new Array();
	ra.push(index.toString());
	ra.push(record.username);
	ra.push(record.description);
	ra.push(user_status_display(record.is_active));
	ra.push(record.msg_num.toString());
	ra.push(record.is_can_weblogin.toString());
	ra.push(record.is_can_post.toString());
	ra.push(record.is_need_check.toString());
	ra.push("\r\n");
	ra.join(",");
	file.writeUTFBytes(ra.join(",")); 
	index++;
	var rowCount:int =  record.children.length;
	for(var r:int=0; r<rowCount; r++) {  
		index = export_user_item(index, record.children[r], file);
	}
	return index;
}

private function msg_status_display(status:int):String{
	switch(status){
		case 1:
			return "待审核";
		case 2:
			return "已发送";
		case 3:
			return "已拒绝";
		case 4:
			return "待发送";
		case 5:
			return "被删除";
		case 6:
			return "被取消";
		case 7:
			return "发送失败";
	}
	return "未知";
}

private function user_status_display(status:int):String{
	switch(status){
		case 1:
			return "活动";
		case 0:
			return "禁用";
	}
	return "活动";
}

private function change_view_stack(view:String):void{
	if(view == "message_send"){
		this.request({q:'userinfo', sid:this.session});
		ViewStack_main.selectedChild = viewpage_message_send;
		if(message_content_input != null)
			message_content_input.text = "";
		message_phone_number.removeAll();
		if(message_content_count != null)
			message_content_count.text = "总字数: 0  拆分条数: 0  联系人数: 0  总条数: 0";
		if(message_new_number != null)
			message_new_number.text = "";
	} else if (view == "message_check"){
		request_listcheckmsg();
		ViewStack_main.selectedChild = viewpage_message_manage;
	} else if(view == "message_send_log"){
		ViewStack_main.selectedChild = viewpage_message_send_log
		if(message_send_log_date_from != null)
			message_send_log_date_from.selectedDate = new Date();
		if(message_send_log_date_to != null)
			message_send_log_date_to.selectedDate = new Date();
		if(message_send_log_status_select != null)
			message_send_log_status_select.selectedIndex = 0;
		message_log_data.removeAll();
	} else if(view == "message_report"){
		ViewStack_main.selectedChild = viewpage_message_report;
		if(message_report_send_user != null)
			message_report_send_user.text = "";
		if(message_report_date_from != null)
			message_report_date_from.selectedDate = new Date();
		if(message_report_date_to != null)
			message_report_date_to.selectedDate = new Date()	
		message_phone_number.removeAll();
			
	} else if(view == "addmsglog"){
		ViewStack_main.selectedChild = viewpage_addmessage_log;
		if(addmessage_log_date_to != null)
			addmessage_log_date_to.selectedDate = new Date()	
		if(addmessage_log_date_from != null)
			addmessage_log_date_from.selectedDate = new Date()	
		message_phone_number.removeAll();
		
	} else if (view == "usermanage") {
		if(message_add_input != null)
			message_add_input.text = "";
		ViewStack_main.selectedChild = viewpage_user_manage;
	} else if (view == "manage_phonenumber"){
		ViewStack_main.selectedChild = viewpage_manage_phonenumber;
		import_phone_number_from_notesbook();
	} else if (view == "upload_report"){
		ViewStack_main.selectedChild = viewpage_upload_report;
		
	} else if (view == "channel_report" ) {
		ViewStack_main.selectedChild = viewpage_channel_report;
		if(channel_report_date_from != null)
			channel_report_date_from.selectedDate = new Date();
		if(channel_report_date_to != null)
			channel_report_date_to.selectedDate = new Date()	
		message_phone_number.removeAll();
	}
		
}

private function check_char_count(text:TextArea, count:Label, address:String):void{

	var i:int = text.text.length;
	var p:int = 0;
	if(i == 0)
		p = 0;
	else if(i <= 70)
		p = 1;
	else 
		p = (i - 1) / 65 + 1;
	
	var dp:Array = message_phone_number.source;

	var n:int = 0;
	
	for ( var j:int = 0; j < dp.length; j++) {
		//if ( dp[j].check == true )
			n += dp[j].count;
	}
	
	var num:int = p * n;
	count.text = "短信字数:" + (i as int).toString() + 
		" 拆分条数: " + (p as int).toString() + 
		" 联系人数: " + (n as int).toString() + 
		" 总条数: " + (num as int).toString();
}
// added by hzhou
private function report_query(username:String, start:Date, end:Date): void {
	//user_manage_viewstack.selectedChild = user_list_data_grid_view;
	
	if(start.time > end.time)
	{
		Alert.show("起始日期必须大于或等于截至日期");
		return;
	}
	//trace(username, start.toString(), end.toString(), type.toString();
	this.request({q:'queryreport',sid:this.session, user:username, begin:start.time, end:end.time});	
}

private function upload_msg_report_query(username:String, start:Date, end:Date): void {
	//user_manage_viewstack.selectedChild = user_list_data_grid_view;
	
	if(start.time > end.time)
	{
		Alert.show("起始日期必须大于或等于截至日期");
		return;
	}
	//trace(username, start.toString(), end.toString(), type.toString();
	this.request({q:'uploadreport',sid:this.session, user:username, begin:start.time, end:end.time});	
}

private function processor_queryreport(param:Object):void{		
	// param format should be :send_user:send_num:success_num:fail_num:append_num
	if(param.errno != 0)
		Alert.show("遇到未知错误");
	else{
		var dp:Array = new Array;
		for (var j:int = 0;j < param.msg.length; j++){
			var co:Object = param.msg[j];
			co.check = false;
			dp.push(co);
		}
		message_phone_number.source = dp;
	}
}

private function processor_uploadreport(param:Object):void{		
	// param format should be :send_user:send_num:success_num:fail_num:append_num
	if(param.errno != 0)
		Alert.show("遇到未知错误");
	else{
		var dp:Array = new Array;
		for (var j:int = 0;j < param.msg.length; j++){
			var co:Object = param.msg[j];
			co.check = false;
			dp.push(co);
		}
		message_phone_number.source = dp;
	}
}

private function channel_report_query(start:Date, end:Date): void {
	if ( start.time > end.time ) {		
		Alert.show("起始日期必须大于或等于截至日期");
		return;
	}
	
	this.request({q:'channelqueryreport',sid:this.session, begin:start.time, end:end.time});	
}

private function processor_channelqueryreport(param:Object):void{
	if ( param.errno != 0) {
		Alert.show(err_str[param.errno]);
	} else {
		var dp:Array = new Array();
		for ( var j:int = 0; j < param.result.length; j++) {			
			var co:Object = param.result[j];
			co.channel = channel_select_data[get_channel_index(co.channel)].label
			co.check = false;
			dp.push(co);
		}
		message_phone_number.source = dp;
	}
}

private function add_all_phonenumber():void{
	check_char_count(message_content_input, message_content_count, get_address_str());
}

private function filter_not_valid_phone_number():void{
	check_char_count(message_content_input, message_content_count, get_address_str());
}

private function filter_same_phone_number():void{
	var dp:Array = message_phone_number.source;
	var addrs:Array = new Array();
	var addrs_tmp:Array = new Array();
	var tmp:Array = new Array();
	var tmpstr:String = "";
	for(var i:int = 0;i < dp.length;i++){
		dp[i].check = false;
		if ( dp[i].type == PHONE_NAME ) {
			addrs.push(dp[i]);
		} else {			
			tmp.push(dp[i].number);
		}
	}
	addrs.sort();
	for(i = 0;i < addrs.length;i++) {
		if(tmpstr != addrs[i].name){
			addrs_tmp.push(addrs[i]);
		}
		tmpstr = addrs[i].name;
	}
	tmp.sort();
	for(i = 0;i < tmp.length;i++){
		if(tmpstr != tmp[i])
			addrs_tmp.push({check:false, number:tmp[i], count:1, type:PHONE_NUMBER});
		tmpstr = tmp[i];
	}
	message_phone_number.source = addrs_tmp;
	check_char_count(message_content_input, message_content_count, get_address_str());
}

[Bindable] private var channel_enabled:Boolean;
[Bindable] private var role_enabled:Boolean;
[Bindable] private var user_enabled:Boolean;
private function channel_enable():void{
	if(this.user_flags != 7)
		channel_enabled = false;
	else
		channel_enabled =  true;
	
	if(this.user_flags != 0)
		user_enabled = true;
	else
		user_enabled =  false;
}


private function role_enable():void{
	var dp:Array = children_user_source;
	role_enabled = false;
	if(dp == null){
		
		return;
	}
	for (var j:int = 0;j < dp[0].children.length; j++){
		var co:Object = dp[0].children[j];
		if(co.username == select_username)
			role_enabled = true;
	}
	if(this.user_name == 'root' && select_username == 'root')
		role_enabled = true;
}


private function addmsglog_query(start:Date, end:Date): void {
	//user_manage_viewstack.selectedChild = user_list_data_grid_view;
	
	if(start.time > end.time)
	{
		Alert.show("起始日期必须大于或等于截至日期");
		return;
	}
	//trace(username, start.toString(), end.toString(), type.toString();
	this.request({q:'addmsglog',sid:this.session, begin:start.time, end:end.time});	
}

private function processor_addmsglog(param:Object):void{		
	// param format should be :send_user:send_num:success_num:fail_num:append_num
	if(param.errno != 0)
		Alert.show("遇到未知错误");
	else{
		var dp:Array = new Array;
		for (var j:int = 0;j < param.msg.length; j++){
			var co:Object = param.msg[j];
			co.check = false;
			dp.push(co);
		}
		message_phone_number.source = dp;
	}
}
// save current phone number address to client's database
private function save_phonenumber(phonelist_name:String, address:Array):void{	
	if ( address.length == 0 ) {
		return;
	}
	
	var add_str:String = address.join(";");
	this.request_addaddresslist(phonelist_name, add_str);
}

private function save_temp_phonenumber(phone_number:ArrayCollection):void{	
		var source:Array = phone_number.source;
	if ( source.length == 0 ) {
		return;
	}

	var address:Array = source.map(toAddress);
	var add_str:String = address.join(";");
	this.request_addaddresslist("temp", add_str);
}

private function request_addaddresslist(phonelist_name:String, number:String):void{
	this.request({q:'addaddresslist', sid:this.session, name:phonelist_name, addresslist:number});
}

private function processor_addaddresslist(param:Object):void{	
	if ( param.errno != 0 ) {
		Alert.show("遇到未知错误");		
	}
	
	var adds_size:int = adds_array.length;
	addresslist_data.addItem({name:phonelist_name.text, count:adds_size, check:false});
}

private function is_selected(item:*, index:int, array:Array):Boolean{
	return item.check == true;	
}

private function toName(element:*, index:int, arr:Array):String {
	return element.name;
}

private function delete_phonenumber_fromlist():void{
	var newsource:Array = addresslist_data.source.filter(is_not_selected);
	var target:Array = addresslist_data.source.filter(is_selected);
	if ( target.length == 0 ) {
		Alert.show("请选择手机集合");
		return;
	}
	var dp:Array = new Array();
	for (var j:int = 0;j < newsource.length; j++){
		var co:Object = newsource[j];
		co.selected = 0;
		dp.push(co);
}
	addresslist_data.source = newsource;
	var address:Array = target.map(toName);
	var add_str:String = address.join(";");
	this.request_deleteaddresslist(add_str);
}

private function request_deleteaddresslist(addresslist:String): void {	
	this.request({q:'deleteaddresslist', sid:this.session, addresslist:addresslist});
}

private function processor_deleteaddresslist(param:Object):void{	
	if ( param.errno != 0 ) {
		Alert.show("遇到未知错误");	
	}
}

private function deleteall_phonenumber():void{
	var source:Array = addresslist_data.source;
	if ( source.length == 0 ) {
		return;
	}
	
	var newsource:Array = new Array();
	addresslist_data.source = newsource;
	var address:Array = source.map(toName);
	var add_str:String = address.join(";");
	this.request_deleteaddresslist(add_str);
}

private function import_phone_number_from_notesbook():void{
	this.request({q:'getaddresslistinfo', sid:this.session});
}

private function processor_getaddresslistinfo(param:Object): void {	
	var dp:Array = new Array;
	for (var j:int = 0;j < param.list.length; j++){
		var co:Object = param.list[j];
		co.selected = 0;
		co.number = param.list[j].name;
		co.type = PHONE_NAME;
		message_phone_number.addItem(co);
		dp.push(co);
	}
	addresslist_data.source = dp;
}

private var adds_array:Array = new Array();

private function import_phone_number_from_file_to_notebook():void{
	if (phonelist_name.text.length == 0) {
		Alert.show("集合名称为空，请输入集合名称。");
		return;
	}
	
	for ( var j:int = 0; j < addresslist_data.length; j++) {
		if ( addresslist_data[j].name == phonelist_name.text ) {
			Alert.show("集合名称已存在，请重新输入。");
			return;
		}
	}
	
	import_phone_number_from_file_to_phone_manage();
	save_phonenumber(phonelist_name.text, adds_array);
}

private function import_phone_number_from_file_to_phone_manage():void{
	address_file = new FileReference();
	address_file.browse();
	
	address_file.addEventListener(Event.SELECT, selectHandler);
	address_file.addEventListener(Event.COMPLETE, completePhoneManageHandler);
}

private function completePhoneManageHandler(event:Event):void
{
	var adds:String = address_file.data.toString();
	adds_array = adds.match(/1[3458]\d{9}/g);
}