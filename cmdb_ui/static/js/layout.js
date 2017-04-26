/**
 * Created by Administrator on 2016/5/19.
 */


var MenuManager = {
    setActiveMenu: function (v) {
        localStorage.setItem('activePage', v);
    },
    getActiveMenu: function () {
        var text = localStorage.getItem('activePage');
        var that = null;

        $('.parentMenu').each(function () {
            if ($(this).text().trim() === text) {
                that = $(this);
                return false;
            }
        });
        return that;
    }
};


// 自动展开 active 菜单
(function () {
    var activeMenu = MenuManager.getActiveMenu();
    if (activeMenu) {
        activeMenu.siblings('.submenu').removeClass('hide');
        activeMenu.attr('active', 'active').removeAttr('display');
    }
})();


$(function() {
    // 菜单的展示和隐藏
    $('.hide').hide().removeClass('hide');
    $('.parentMenu').on('click', function() {
        var $parentmenu = $(this);
        var $submenu = $parentmenu.siblings('.submenu');
        var $activemenu = $('.parentMenu[active="active"]');
        // var $navbar = $('#navbar');
        var speed = 'fast';

        $submenu.slideToggle(speed, function () {
            if ($parentmenu.attr('active')) {
                $parentmenu.removeAttr('active');

                MenuManager.setActiveMenu(null);
            } else {
                $parentmenu.attr('active', 'active');

                MenuManager.setActiveMenu(
                    $parentmenu.text().trim()
                );
            }
        });

        //检查其他菜单，如果有是active的，就关闭菜单.
        if (!$parentmenu.is($activemenu)) {
            $activemenu.siblings('.submenu').slideUp(speed);
            $activemenu.removeAttr('active');
        }
    });

    //个人信息隐藏和展示
    $('#viewUserInfo').on('click', function () {
        var $user = $('#UserInfo');
        if ($user.hasClass('hide')) {
            $user.fadeIn('slow').removeClass('hide');
        } else {
            $user.fadeOut('slow', function () {
                $user.addClass('hide');
            });
        }
    });

    //鼠标指针离开个人信息时就隐藏它
    $('#UserInfo').on('mouseleave', function () {
        $(this).fadeOut('slow', function () {
            $(this).removeAttr('style').addClass('hide');
        });
    });

});




