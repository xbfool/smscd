/**
 * Created with PyCharm.
 * User: xbfool
 * Date: 12-8-9
 * Time: PM4:11
 * To change this template use File | Settings | File Templates.
 */

var smsc_login = function() {
    var username = $("#login_username").val();
    var password = $("#login_password").val();
    $.ajax({
        type:"POST",
        url:$.smsd_url,
        data: JSON.stringify({q:'auth', user:username, pass:$.sha1(password)}),
        contentType: "application/json; charset=utf-8",
        success:function(data) {
            //alert(JSON.stringify(data));

            if(data.sid != "" && data.sid != null ){
                $.smsc.username = data.username;
                $.smsc.sessionid = data.sid;

                $("#dialog").dialog('close');
                //smsc_main_ui();
                $("#main").show();
            }else{
                alert("用户密码错误, 请重新输入");
            }

        },
        dataType:"json"
    });
};

var smsc_logout = function(){
    $.smsc = {};
    smsc_login_ui();
    $("#main").hide();
};