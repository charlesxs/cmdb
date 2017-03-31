/**
 * Created by Administrator on 2016/5/19.
 */

$(function() {
    $('.parentMenu').click(function() {
        var curClass = $(this).siblings('.submenu').attr('class');
        // console.log(curClass);
        // console.log($(this).parent().siblings('.menuIdentity'));

        if (curClass.indexOf('hide') < 0) {
            var curElement = $(this);
            //点击事件发生后如果子菜单是展开的就隐藏, 并且移除父元素的 bgcolor 样式.
            $(this).siblings('.submenu').slideUp('fast', function () {
                curElement.removeClass('bgcolor active');
                $(this).addClass('hide').removeAttr('style');
            });

        } else {
            // 点击事件发生后如果子菜单是隐藏的就展开, 同时找到其他菜单项并隐藏其子菜单.
            $(this).siblings('.submenu').slideDown('fast').removeClass('hide');
            $(this).addClass('bgcolor active');


            $(this).parent().siblings('.GroupSpace').each(function(){
                // $(this).children('.submenu').addClass('hide');
                // $(this).children('.parentMenu').removeClass('bgcolor');

                $(this).children('.submenu').slideUp('fast', function () {
                    $(this).siblings('.parentMenu').removeClass('bgcolor active');
                    $(this).addClass('hide').removeAttr('style');
                });
            })
        }

    }).mouseover(function () {
        var curClass = $(this).siblings('.submenu').attr('class');

        if (curClass.indexOf('hide') >= 0) {
            $(this).addClass('bgcolor');
        }

    }).mouseout(function () {
        var curClass = $(this).siblings('.submenu').attr('class');

        if (curClass.indexOf('hide') >= 0) {
            $(this).removeClass('bgcolor');

        }
    });

    //个人信息隐藏和展示
    $('#viewUserInfo').click(function () {
        var curClass = $('#UserInfo').attr('class');
        if (curClass.indexOf('hide') < 0) {
            $('#UserInfo').removeAttr('style').addClass('hide');
        } else {
            $('#UserInfo').fadeIn('slow').removeClass('hide');
        }
    });

    //鼠标指针离开个人信息时就隐藏它
    $('#UserInfo').mouseleave(function () {
        $(this).fadeOut('fast', function () {
            $(this).removeAttr('style').addClass('hide');
        });
    });


});



