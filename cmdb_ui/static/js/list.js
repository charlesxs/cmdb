/**
 * Created by Administrator on 2016/5/28.
 */

// $() == $(document).ready();
$(function(){
    var checkall = $('#checkall');
    var allbox = $('tbody input[type="checkbox"]');

    // 鼠标滑过表格时着色
    $('tr').mouseover(function(){
      $(this).addClass('movecolor');
    }).mouseout(function () {
        $(this).removeClass('movecolor');
    });

    //搜索
    $('#search-input').keydown(function (event) {
        if (event.keyCode === 13){
            SearchGet();
        }
    });

    $('.search-font').click(function () {
        SearchGet();
    });


    // check all
    checkall.on('click', function () {
        allbox.each(function () {
            this.checked = checkall[0].checked;
            // $(this).attr('checked', !checkall.checked);
        })
    });

    // 当某一个checkbox取消checked的时候, 取消 check all
    allbox.click(function () {
        if (this.checked === false ) {
            checkall[0].checked = false;
        }
    });
});


var Pager = {
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


function SearchGet(){
    var value = $('#search-input').val().trim();
    if(value !== ""){
        var root_path = location.pathname.split('/').slice(0, 2).join('/') + '/';
        $.get(root_path, {keyword: value}, function (data) {
            // 替换整个当前页面
            $(document).find("html").html(data);
        } )
    }
}

//
// function SearchPost() {
//    if ($('#search-input').val() != ""){
//         var keyAry = window.location.href.split('/');
//         for (i in keyAry){
//             if (keyAry[i].indexOf('list')>0){
//                 var key = keyAry[i].split('_')[0];
//             }
//         }
//
//         var csrftoken = getCookie('csrftoken');
//         $.ajaxSetup({
//             beforeSend: function (xhr) {
//                 if (!this.crossDomain) {
//                     xhr.setRequestHeader("X-CSRFToken", csrftoken);
//                 }
//             }
//         });
//
//         $.post('/mytest/search/',
//                {search: $('#search-input').val(), searchtype: key},
//                function (data) {
//                    // $(document).find("html").html(data);
//                    $('tbody').html(data);
//         })
//    } else {
//         if ($('tbody').html().trim() == "") {
//             location.reload();
//         }
//    }
// }
//
// function getCookie(name) {
//     var cookieValue = null;
//     if (document.cookie && document.cookie != '') {
//         var cookies = document.cookie.split(';');
//         for (var i = 0; i < cookies.length; i++) {
//             var cookie = jQuery.trim(cookies[i]);
//             // Does this cookie string begin with the name we want?
//             if (cookie.substring(0, name.length + 1) == (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }



(function () {
    // 渲染表格背景色
    $('tr:even').addClass('eventcolor');
    $('tr:odd').addClass('oddcolor');

    //给当前分页按钮着色
    var current = Pager.get_page_num();
    Pager.pages.each(function (i) {
        if (current === 1 && i === 0){
            $(this).addClass('disabled');
            $(this).children().attr('href', '#');
        }

        if (parseInt($(this).text()) === current) {
           $(this).children().addClass('page-color');
        }
    });
})();