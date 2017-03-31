/**
 * Created by Administrator on 2016/5/18.
 */

//动态显示登录框
function visit_login(){
    if (current != end){
        current += 1;
        $('#main-window').css('margin-top', current.toString() + 'px');
    } else {
        clearInterval(sobj);
    }
};

(function () {
    // 淡入
    $('#main-window').fadeIn('fast');

    var hg = $('#main-window').css('margin-top');
    end = parseInt(hg.substring(0, hg.length - 2));
    current = end - 10;
    sobj = setInterval("visit_login()", 50);
})();


//DOM加载完后开始注册事件
$(function() {
    $('input[name="username"]').blur(show_error).focus(hide_error);

    $('input[name="password"]').blur(show_error).focus(hide_error);

    $('input[name="password"]').keydown(function(event) {
        if (event.keyCode == 13) {
            if (show_error(event, $(this))) {
                Ajax_post();
            }
        } else {
            hide_error(event, $(this));
        }
    });

    $('.login-button').click(Ajax_post);
});


//事件函数: 检测用户名或密码为空时, 显示错误提示
function show_error() {
    if (!arguments[1]) {
        var obj = $(this);
    } else {
        var obj = arguments[1];
    }

    if (obj.val().trim() == "") {
        obj.siblings(".error-prompt").removeClass('hide');
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

    obj.siblings(".error-prompt").addClass("hide");
}

//使用Ajax请求服务器来代替submit 整个页面提交.
function Ajax_post() {
        var user = $('input[name="username"]').val();
        var pwd = $('input[name="password"]').val();

        //使用Ajax验证用户名和密码如果用户名和密码都正确则跳转到相对应页面, 否则提示错误.
        if (user != "" && pwd != "") {
            $.post('/mytest/login/', {username: user, password: pwd}, function (data) {
                var data = jQuery.parseJSON(data);

                switch (data.status) {
                    case "200":
                        window.location.href = data.url;
                        break;
                    case "404":
                        $('#uError').removeClass('hide');
                        $('input[name="password"]').val("");

                        $('#uError').fadeOut(3000, function() {
                            $(this).addClass('hide');
                            $(this).removeAttr('style');
                        });
                        break;
                    default:
                        $('#uError').children('.font-prompt').html('*服务器偷懒中...');
                        $('#uError').removeClass('hide');
                        $('input[name="password"]').val("");

                        $('#uError').fadeOut(7000, function() {
                            $(this).addClass('hide');
                            $(this).removeAttr('style');
                        });
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
