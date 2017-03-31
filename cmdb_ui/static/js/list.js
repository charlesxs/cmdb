/**
 * Created by Administrator on 2016/5/28.
 */

// $() == $(document).ready();
$(function(){
    // 鼠标滑过表格时着色
    $('tr').mouseover(function(){
      $(this).addClass('movecolor');
    }).mouseout(function () {
        $(this).removeClass('movecolor');
    });


    //鼠标滑过分页按钮时着色
    $('.page-border .page-button').mouseover(function(){
      $(this).addClass('page-color');
    }).mouseout(function () {
        $(this).removeClass('page-color');
    });

    //搜索
    $('#search-input').keydown(function (event) {
        if (event.keyCode == 13){
            SearchGet();
        }
    });

    $('.search-font').click(function () {
        SearchGet();
    }).mouseout(function () {
        $('.search').removeClass('mouse-color');
    }).mouseover(function () {
        $('.search').addClass('mouse-color');
    });

    
    $('tbody input[type="checkbox"]').click(function () {
        if ($(this).attr('checked') == undefined ) {
            $('#checkall').attr('checked', false);
        }
    });
    // $('#search-input').focus(search.enter).blur(search.leave);
});

// var search = new Search($('#search-input'));
// function Search(ipt){
//     var value = $(ipt).val();
//     this.enter = function () {
//         if ($(ipt).val() == value) {
//             $(ipt).val("");
//             $(ipt).removeClass('prompt-font');
//         }
//     };
//
//     this.leave = function () {
//         if ($(ipt).val() == ""){
//             $(ipt).val(value);
//             $(ipt).addClass('prompt-font');
//         }
//     };
// }

function SearchGet(){
    var value = $('#search-input').val();
    if(value != ""){
        $.get(window.location.pathname, {keyword: value}, function (data) {
            // 替换整个当前页面
            $(document).find("html").html(data);

            // 渲染第一页按钮颜色并取消其他页按钮颜色
              $('.page-button').each(function(){
                if ($(this).html() == 1){
                    $(this).addClass('current-page-color');
                } else{
                    if($(this).attr('class').indexOf('current-page-color') >0){
                        $(this).removeClass('current-page-color');
                    }
                }
            });
        } )
    } else {
        location.reload();
    }
}


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


 //全选和全不选
 function checkAll(chkObj) {
        var checks = document.getElementsByName('infoList');
        for (i in checks){
            checks[i].checked = chkObj.checked;
        };
};


(function () {
    // 渲染表格背景色
    $('tr:even').addClass('treventcolor');
    $('tr:odd').addClass('troddcolor');

    //给当前分页按钮着色
    var ref = window.location.href.split('=');
    var currentPage = ref[ref.length-1];
    if (currentPage.search("^[0-9]+$") < 0) {
        currentPage = 1;
    };
    $('.page-button').each(function(){
        if ($(this).html() == currentPage){
            $(this).addClass('current-page-color');
        }
    });


    // 动态导航栏信息
    var navAry = [];
     $('.active').next().children().children().each(function () {
        if (window.location.href.indexOf($(this).attr('href')) >= 0) {
             navAry.push('Dashboard', $('.active span').html(), $(this).html());
        }
    });
    newNavigation = navAry.join(' / ');
    $('.nav-content').html(newNavigation);

})();