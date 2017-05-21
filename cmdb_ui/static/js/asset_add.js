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
   var $asset_type = $('#asset_type_select');
   var $networkdevice = $('#networkdevice');
   var $server = $('#server');
   var $route = $('#route');
   var $submit_button = $('#submit_button');
   var $form = $('form');
   var $required = $('input[aria-required="true"]');

   $asset_type.on('change', function () {
       var type = $asset_type.find("option:selected").text();
       var check_device = ['交换机', '路由器', '其他网络设备'];
       if (check_device.indexOf(type) >=0 && $networkdevice.hasClass('hidden')) {
           $networkdevice.removeClass('hidden');
           $server.addClass('hidden');
           $route.val('networkdevice');
       } else if (check_device.indexOf(type) < 0 && $server.hasClass('hidden')) {
           $server.removeClass('hidden');
           $networkdevice.addClass('hidden');
           $route.val('server')
       }
   });
   
   $submit_button.on('click', function () {
       if (checkNull($required, $server, $networkdevice)){
           $form.submit();
       }
   });

   $required.on('change', function () {
        var selector = 'span[bind_name=' + this.name + ']';
        if (!$(selector).hasClass('hidden')) {
           $(selector).addClass('hidden');
       }
   });

});