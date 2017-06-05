/**
 * Created by charles on 2017/4/21.
 */

(function () {
    var $failed = $('#alert-danger');
    var $success = $('#alert-success');

    if (!$failed.hasClass('hidden')) {
        setTimeout("$('#alert-danger').fadeOut(2000)", 3000);
    }
    if (!$success.hasClass('hidden')) {
        setTimeout("$('#alert-success').fadeOut(2000)", 1000);
    }

})();


function checkNull($required, $server, $networkdevice) {
    var submit = true;
    var selector = null;

    $required.each(function (index, obj) {
        switch (0) {
            case obj.name.indexOf('server'):
                if ($server.hasClass('hidden')) {
                    return true;
                }

                if (!$(obj).val()) {
                    selector = 'span[bind_name={}]'.format(obj.name);
                    $(selector).removeClass('hidden');
                    submit = false;
                    return false;
                }
                break;
            case obj.name.indexOf('networkdevice'):
                if ($networkdevice.hasClass('hidden')) {
                    return true;
                }
                if (!$(obj).val()){
                    selector = 'span[bind_name={}]'.format(obj.name);
                    $(selector).removeClass('hidden');
                    submit = false;
                    return false;
                }
                break;
            default:
                if (!$(obj).val()){
                    selector = 'span[bind_name={}]'.format(obj.name);
                    $(selector).removeClass('hidden');
                    submit = false;
                    return false;
                }
        }

    });
    return submit;
}


$(function () {
   // var $asset_type = $('#asset_type_select');
   var $networkdevice = $('#networkdevice');
   var $server = $('#server');
   // var $route = $('#route');
   var $submit_button = $('#submit_button');
   var $form = $('form');
   var $required = $('input[aria-required="true"]');

   // $asset_type.on('change', function () {
   //     var type = $asset_type.find("option:selected").text();
   //     var check_device = ['交换机', '路由器', '其他网络设备'];
   //     if (check_device.indexOf(type) >=0 && $networkdevice.hasClass('hidden')) {
   //         $networkdevice.removeClass('hidden');
   //         $server.addClass('hidden');
   //         $route.val('networkdevice');
   //     } else if (check_device.indexOf(type) < 0 && $server.hasClass('hidden')) {
   //         $server.removeClass('hidden');
   //         $networkdevice.addClass('hidden');
   //         $route.val('server')
   //     }
   // });

   $submit_button.on('click', function () {
       if (checkNull($required, $server, $networkdevice)){
           $form.submit();
       }
   });

   $required.on('change', function () {
        // var selector = 'span[bind_name=' + this.name + ']';
        var selector = 'span[bind_name="{0}"]'.format(this.name);
        if (!$(selector).hasClass('hidden')) {
           $(selector).addClass('hidden');
       }
   });

    // 基本信息和硬件信息之前切换
    $('.info').on('click', '.info-block', function (e) {
        var $block = $(e.target);
        var $selected = $('.info-block-selected');

        // 去除之前信息的选中状态，并将其相对应的 table 隐藏
        $('.none-class[info="{0}"]'.format($selected.attr('info'))).addClass('hidden');
        $selected.removeClass('info-block-selected');

        // 添加当前信息的选中状态，并将其对应的 table 展示
        $('.none-class[info="{0}"]'.format($block.attr('info'))).removeClass('hidden').removeAttr('style');
        $block.addClass('info-block-selected');
    });

    // 动态添加 内存，网卡，CPU 和磁盘 DOM节点
    $('button[add="add"]').on('click', function () {
        var names = {
            '网卡': 'n',
            '内存': 'm',
            'CPU': 'c',
            '磁盘': 'd'
        };
        var key = $(this).text().slice(4);
        var old_id = $('fieldset[{0}="{1}"]'.format(names[key], names[key])).last().attr('id');
        var num = parseInt(old_id.match(/[0-9]+$/)[0]) + 1;
        var new_name = names[key] + num;
        var $template = $('#{0}1'.format(names[key]));
        var template_id = names[key] + 1;
        var $new_dom = $template.clone();
        // debugger;

        // 修改 id
        $new_dom.attr('id', new_name);
        $new_dom.children('legend').text(key + num);

        // 添加 删除按钮
        $new_dom.children('button.add-info').addClass('btn-danger').removeClass('hidden');

        // 修改 label for 属性
        $new_dom.find('label').each(function (i, e) {
            var $label = $(e);
            var value = $label.attr('for').replace(template_id, new_name);
            $label.attr('for', value);
        });

        // 修改 input name 属性
        $new_dom.find('input.form-control').each(function (i, e) {
            var $input = $(e);
            var value = $input.attr('name').replace(template_id, new_name);
            $input.attr('name', value);
        });

        // 修改 select name 属性
        $new_dom.find('select.form-control').each(function (i, e) {
           var $select = $(e);
           var value = $select.attr('name').replace(template_id, new_name);
           $select.attr('name', value);
        });

        // 插入修改后的dom
        $('#{0}{1}'.format(names[key], num - 1)).after($new_dom);
    });

    // 动态删除网卡 input
    $('#hard').on('click', '.btn-danger', function (e) {
        $(e.target).parent().remove();
    })

});