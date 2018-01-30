/**
 * Created by kido on 2016/9/22.
 */

function app_alert(text) {
    var d = dialog({
        width: 650,
        title: '结果',
        ok: function () {
            window.location.reload()
        },
        okValue: '关闭',
        content: '<div class="king-notice-box king-notice-warning"><p class="king-notice-text" style="word-break: break-all;width:100%">' + text + '</p></div>'
    });
    d.showModal();
}

function app_none_modal_alert(text) {
    var d = dialog({
        width: 260,
        title: '提示',
        ok: function () {
        },
        okValue: '确定',
        content: '<div class="king-notice-box king-notice-warning"><p class="king-notice-text">' + text + '</p></div>'
    });
    d.show();
}



function show_loading() {

    $('#loading').css('display', 'block')
}

function close_loading() {
    $('#loading').css('display', 'none')
}

function auto_height(minus_height) {
    var winHeight = 0;
    if (window.innerHeight)
        winHeight = window.innerHeight;
    if (document.documentElement && document.documentElement.clientHeight && document.documentElement.clientWidth) {
        winHeight = document.documentElement.clientHeight;
    }
    return winHeight - minus_height;
}

//时间格式化
Date.prototype.Format = function (fmt) { //author: meizz  
    var o = {
        "M+": this.getMonth() + 1, //月份         
        "d+": this.getDate(), //日        
        "h+": this.getHours(), //小时        
        "m+": this.getMinutes(), //分        
        "s+": this.getSeconds(), //秒  
        "q+": Math.floor((this.getMonth() + 3) / 3), //季度    
        "S": this.getMilliseconds() //毫秒     
    };
    if (
        /(y+)/.test(fmt)
    )
        fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o)
        if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
    return fmt;
};

function ChanegeToPercent(num) {
    if (num == 0) {
        return num
    }
    if (/\d+\.?\d+/.test(num)) {

    }
    var result = (num * 100).toString(),
        index = result.indexOf(".");
    if (index == -1 || result.substr(index + 1).length <= 4) {
        return result;
    }
    return result.substr(0, index + 2);
}


// function auto_update() {
//     $.post(site_url + "test/", {}, function (res) {
//         setTimeout(auto_update, 900000);
//     })
// }
// auto_update();

// $(function () {
//     if (app_path){
//         $.post(site_url + 'auto_update_url/', {window_url: app_path}, function (res) {
//
//         })
//     }
// });