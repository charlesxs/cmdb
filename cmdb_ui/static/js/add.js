/**
 * Created by charles on 2017/4/25.
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

function checkNull($required) {
    var submit = true;
    var selector = null;

    $required.each(function (index, obj) {
        if (!$(obj).val()){
            selector = 'span[bind_name=' + obj.name + ']';
            $(selector).removeClass('hidden');
            submit = false;
            return false;
        }

    });
    return submit;
}

$(function () {
    var $submit_button = $('#submit_button');
    var $form = $('form');
    var $required = $('input[aria-required="true"]');

    $submit_button.on('click', function () {
        if (checkNull($required)) {
            $form.submit();
        }
    });

    $required.on('change', function () {
        var selector = 'span[bind_name=' + this.name + ']';
        if (!$(selector).hasClass('hidden')) {
            $(selector).addClass('hidden');
        }
    })
});
