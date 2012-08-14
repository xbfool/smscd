/**
 * Created with PyCharm.
 * User: xbfool
 * Date: 12-8-14
 * Time: AM10:14
 * To change this template use File | Settings | File Templates.
 */

var smsc_login_ui = function() {
    $("#dialog").load("login.html", function(){
        $("#login_button").button().bind('click', function() {
            smsc_login();
        });
        $("#dialog").dialog();
    });
    //$("#main").hide();
};

var smsc_main_ui = function() {
    $("#sidebar").load("sidebar.html", function(){
        //$("#sidebar").accordion('destory');
        $("#sidebar").accordion();
        $("#message_send").button().bind('click',
            function() {smsc_message_send_ui();}
        );
        $("#special_send").button().bind('click',
            function() {smsc_special_send_ui();}
        );
        $("#special_send2").button().bind('click',
            function() {smsc_special_send_ui();}
        );
        $("#message_send_status").button().bind('click',
            function() {smsc_special_send_ui();}
        );
        $("#statics_all").button().bind('click',
            function() {smsc_special_send_ui();}
        );
        $("#add_money_record").button().bind('click',
            function() {smsc_special_send_ui();}
        );
        $("#contact_manage").button().bind('click',
            function() {smsc_special_send_ui();}
        );
        $("#uplod_message_record").button().bind('click',
            function() {smsc_special_send_ui();}
        );
        $("#channel_report").button().bind('click',
            function() {smsc_special_send_ui();}
        );
        $("#user_manage").button().bind('click',
            function() {smsc_special_send_ui();}
        );
        $("#change_password").button().bind('click',
            function() {smsc_special_send_ui();}
        );
        $("#admin_page").button().bind('click',
            function() {smsc_special_send_ui();}
        );
        $("#logout").button().bind('click',
            function() {smsc_logout();}
        );
    })
};

var smsc_message_send_ui = function() {
    alert("message_send");
};

var smsc_special_send_ui = function() {
    alert("special_send");
};