/**
 * Created by Administrator on 2016/5/19.
 */


String.prototype.format = function() {
    var pat = /{.*?}/;
    var newstr = this;
    for (var i=0; i<arguments.length; i++) {
        newstr = newstr.replace(pat, arguments[i]);
    }
    return newstr;
};


var MenuRecoder = {
    setActiveMenu: function (v) {
        localStorage.setItem('activePage', v);
    },
    getActiveMenu: function () {
        var text = localStorage.getItem('activePage');
        var $that = null;

        $('.parentMenu').each(function () {
            if ($(this).text().trim() === text) {
                $that = $(this);
                return false;
            }
        });
        return $that;
    }
};


var MenuManager = {
    active: function ($menu) {
        // 设置 active 属性
        $menu.attr('active', 'active');

        // 将 加号 换成 减号
        $menu.children('.fa')
            .removeClass('fa-plus')
            .addClass('fa-minus');
    },

    unactive: function ($menu) {
        // 去除 active 属性
        $menu.removeAttr('active');

        // 将减号替换成加号
        $menu.children('.fa')
            .removeClass('fa-minus')
            .addClass('fa-plus');
    }
};


// 自动展开 active 菜单
(function () {
    var $activeMenu = MenuRecoder.getActiveMenu();
    if ($activeMenu) {
        $activeMenu.siblings('.submenu').removeClass('hide').removeAttr('display');
        MenuManager.active($activeMenu);
    }
})();


$(function() {
    // 菜单的展示和隐藏
    $('.hide').hide().removeClass('hide');
    $('.parentMenu').on('click', function() {
        var $parentmenu = $(this);
        var $submenu = $parentmenu.siblings('.submenu');
        var $activemenu = $('.parentMenu[active="active"]');
        var speed = 'fast';

        $submenu.slideToggle(speed, function () {
            if ($parentmenu.attr('active')) {
                MenuManager.unactive($parentmenu);
                MenuRecoder.setActiveMenu(null);
            } else {
                MenuManager.active($parentmenu);
                MenuRecoder.setActiveMenu(
                    $parentmenu.text().trim()
                );
            }
        });

        //检查其他菜单，如果有是active的，就关闭菜单.
        if (!$parentmenu.is($activemenu)) {
            MenuManager.unactive($activemenu);
            $activemenu.siblings('.submenu').slideUp(speed);
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

    // logout 时去除活动菜单记录
    $('#logout').on('click', function () {
        MenuRecoder.setActiveMenu(null);
    })
});




