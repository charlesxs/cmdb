/**
 * Created by charles on 2017/6/11.
 */

(function () {
    $('td+td').each(function () {
        var $that = $(this);
        if ($that.text()) {
            $that.addClass('blue');
        }
    })
})();

