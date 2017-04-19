/**
 * Created by Administrator on 2016/5/18.
 */

//动态显示登录框
function visit_login(){
    if (current !== end){
        current += 1;
        $('#main-window').css('margin-top', current.toString() + 'px');
    } else {
        clearInterval(sobj);
    }
}

(function () {
    // 淡入
    $('#main-window').fadeIn('fast');

    var hg = $('#main-window').css('margin-top');
    end = parseInt(hg.substring(0, hg.length - 2));
    current = end - 10;
    sobj = setInterval("visit_login()", 50);
})();



//DOM加载完后开始注册事件
$(function($) {
    var user = $('input[name="username"]');
    var password = $('input[name="password"]');


    user.blur(show_error).focus(hide_error);
    password.blur(show_error).focus(hide_error);

    password.keydown(function(event) {
        if (event.keyCode == 13) {
            if (show_error(event, $(this))) {
                Ajax_post(user, password);
            }
        } else {
            hide_error(event, $(this));
        }
    });

    $('.login-button').click(function () {
        Ajax_post(user, password);
    });
});


//事件函数: 检测用户名或密码为空时, 显示错误提示
function show_error() {
    if (! arguments[1]) {
        var obj = $(this);
    } else {
        var obj = arguments[1];
    }

    if (!obj.val().trim()) {
        var ue = obj.siblings('#uError');
        if (!ue.hasClass('hide')){
            ue.addClass('hide');
        }

        obj.siblings(".none-error").removeClass('hide');
        return false;
    }
    return true;
}

//事件函数: 当焦点进入文本框时取消错误提示.
function hide_error() {
    if (!arguments[1]) {
        var obj = $(this);
    } else {
        var obj = arguments[1];
    }

    obj.siblings(".none-error").addClass("hide");
}

//使用Ajax请求服务器来代替submit 整个页面提交.
function Ajax_post(user, password) {
    // debugger;
    var username = user.val().trim();
    var pwd = password.val().trim();
    var e = $('#uError');
    //使用Ajax验证用户名和密码如果用户名和密码都正确则跳转到相对应页面, 否则提示错误.
    if (username && pwd) {
        $.post('/login/', {username: username, password: pwd}, function (data) {
            // var data = $.parseJSON(data);

            switch (data.status) {
                case 200:
                    location.href = data.url;
                    break;
                case 404:
                    e.text("* 没有此用户");
                    e.removeClass('hide');
                    password.val("");
                    break;
                default:
                    e.text('* 密码输入错误');
                    e.removeClass('hide');
                    password.val("");
                    break;
            }
        });
    }
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = doucment.cookie.split(';');
        for (var i=0;i<cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length+1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

