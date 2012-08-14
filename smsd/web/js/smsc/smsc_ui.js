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
    $("#main").hide();
};

var smsc_main_ui = function() {
    $("#main").show();
};