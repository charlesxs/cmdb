/**
 * Created by charles on 2017/6/23.
 */


(function () {
    sessionStorage.setItem('search_obj', 1);
})();


$(function () {
    var $advance_search_add = $('.advance-search-add');
    var $advance_search_example = $('#advance-search-example');
    var $advance_search = $('.advance-search');

    $advance_search_add.on('click', function () {
        //检查是否要添加, 最多只能添加5个
        var num = sessionStorage.getItem('search_obj');
        if (!num) {
            num = 2;
            sessionStorage.setItem('search_obj', num);
        } else if (num < 5){
            num++;
            sessionStorage.setItem('search_obj', num);
        } else {
            $(this).addClass('disabled');
            return false;
        }

        // 添加新的 搜索对象
        var $new_search = $advance_search_example.clone(true);
        $new_search.removeClass('hidden');
        $(this).before($new_search);
    });


    // 实时获取 搜索对象的 有哪些类型或值
    $('.content-header').on('change', '.field', function (e) {
        var $field = $(e.currentTarget);
        var $select_value = $field.siblings('.value');
        var value = $field.val();
        var $new_dom = $('<select name="value" class="value"><option value=""></option></select>');

        if (!value.trim()) {
            $select_value.replaceWith($new_dom);
            return false;
        }

        $.ajax({
            type: 'POST',
            url: '/object_query/',
            dataType: 'json',
            data: {'field': value},
            success: function (data) {
                var d = data.data;
                for (var i=0; i<d.length; i++){
                    $new_dom.append('<option value="{0}">{1}</option>'.format(d[i], d[i]))
                }
                // 新的DOM 替换旧DOM
                $select_value.replaceWith($new_dom);
            }
        });

    });

    // 高级搜索
    $advance_search.on('click', function () {
        var $fields = $('.field');
        var data = {};
        $fields.each(function (i, obj) {
            var $obj = $(obj);
            var $value = $obj.siblings('.value');

            var key = $obj.val();
            var value = $value.val();

            if (key && value){
                data[key] = value;
            }
        });

        // search
        var root_path = location.pathname.split('/').slice(0, 2).join('/');
        var params = urlEncode(data);
        location.href = root_path + params;
    })

});






