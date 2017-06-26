/**
 * Created by Administrator on 2016/5/28.
 */


var PageRecoder = {
    pages: $('ul.pagination').children(),
    get_page_num: function () {
        var path = location.pathname.split('/');
        for (var i=0; i<path.length; i++){
            var page_num = parseInt(path.pop());
            if (!isNaN(page_num)) {
                break;
            }
        }

        if (isNaN(page_num)){
            return 1;
        }
        return page_num;
    }

};


function urlEncode(params) {
    var root = '/?';
    for (var k in params){
        root = root + '{0}={1}&'.format(k, params[k]);
    }
    return root.slice(0, -1);
}


function SearchGet(){
    var value = $('#search-input').val().trim();
    if(value !== ""){
        var root_path = location.pathname.split('/').slice(0, 2).join('/');
        location.href = root_path + urlEncode({'keyword': value});
    }
}


function UndoAlarm(action) {
    var speed = 1000;
    switch (action) {
        case 'success':
            $('.alert-success').fadeOut(speed);
            break;
        case 'failed':
            $('.alert-danger').fadeOut(speed);
            break;
    }
}


function DeleteItem(id, $objs) {
    var $success = $('.alert-success');
    var $failed = $('.alert-danger');

    // 如果没有资产被选中，则退出, 不发请求.
    if (id <= 0 || id.length <= 0){
        $failed.text('没有任何项目被选中 ...');
        $failed.removeClass('hidden').removeAttr('style');
        setTimeout('UndoAlarm("failed")', 1000);
        return ;
    }

    var ids = Array.isArray(id) ? JSON.stringify(id) : JSON.stringify([id]);
    $.ajax({
        type: 'POST',
        url: location.pathname,
        dataType: 'json',
        data: {ids: ids},
        success: function () {
            $objs.remove();
            $success.removeClass('hidden').removeAttr('style');
            setTimeout('UndoAlarm("success")', 1000);
        },
        error: function (msgobj) {
            var msg = JSON.parse(msgobj.responseText).msg;
            $failed.text('删除失败, 理由: ' + msg);
            $failed.removeClass('hidden').removeAttr('style');
            setTimeout('UndoAlarm("failed")', 5000);
        }
    })
}


(function () {
    //给当前分页按钮着色
    var current = PageRecoder.get_page_num();
    PageRecoder.pages.each(function (i) {
        if (current === 1 && i === 0){
            $(this).addClass('disabled');
            $(this).children().attr('href', '#');
        }

        if (parseInt($(this).text()) === current) {
           $(this).children().addClass('page-color');
        }
    });
})();



// $() == $(document).ready();
$(function(){
    var $checkall = $('#checkall');
    var $table = $('.table');
    var $mymodal = $('#alert-modal-sm');

    //搜索
    $('#search-input').keydown(function (event) {
        if (event.keyCode === 13) {
            SearchGet();
        }
    });

    $('.search-font').click(function () {
        SearchGet();
    });


    // check all
    $checkall.on('click', function () {
        $('tbody input[type="checkbox"]').each(function () {
            this.checked = $checkall[0].checked;
        })
    });

    // 当某一个checkbox取消checked的时候, 取消 check all
    $table.on('click', 'tbody input[type="checkbox"]', function (e) {
        var checkbox = e.target;
        if (checkbox.checked === false) {
            $checkall[0].checked = false;
        }
    }).on('click', '.btn-danger', function (e) {
        var $pattr = $(e.target).parents('tr');
        var data_id = $pattr.attr('data-id');
        $mymodal.data('delete-id', data_id).data('delete-obj',
            $pattr).modal();
    });

    // 取出已选择资产，调用模态框，并将数据传给模态框
    $('#deletion-selected').on('click', function () {
        var del_ids = [],
            del_objs = [];

        $('tbody input[type="checkbox"]').each(function (index, obj) {
           if (obj.checked === true) {
               del_ids.push($(obj).val());
               del_objs.push($(obj).parents('tr')[0]);
           }
        });

        $mymodal.data('delete-id', del_ids).data('delete-obj', $(del_objs)).modal();
    });

     // 触发模态框click, 删除所选资产
    $('#btn-modal-yes').on('click', function () {
        $mymodal.modal('hide');
        DeleteItem($mymodal.data('delete-id'), $mymodal.data('delete-obj'));
    });


});