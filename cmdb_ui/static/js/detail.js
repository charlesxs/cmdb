/**
 * Created by charles on 2017/6/4.
 */


$(function () {
    $('.info').on('click', '.info-block', function (e) {
        var $block = $(e.target);
        var $selected = $('.info-block-selected');

        // 去除之前信息的选中状态，并将其相对应的 table 隐藏
        $('.table[info="{0}"]'.format($selected.attr('info'))).addClass('hidden');
        $selected.removeClass('info-block-selected');

        // 添加当前信息的选中状态，并将其对应的 table 展示
        $('.table[info="{0}"]'.format($block.attr('info'))).removeClass('hidden').removeAttr('style');
        $block.addClass('info-block-selected');
    })
});