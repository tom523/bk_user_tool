
var servers_selected = [
];

var content_height = auto_height(100);
var select_server_grid = "";

var os_type = [{id: "W", text: 'Windows'}, {id: "L", text: 'Linux'}];
$("#sys_select .select2_box").select2({data: os_type});

var grid_option = {
    pageable: false,
    dataSource: {
        data: servers_selected
    },
    columns: [
        {field: 'ip', title: 'IP地址'},
        {
            title: '操作', width: 60,
            template: '<div style="width:100%;text-align: center;"><a class="fa fa-trash-o" style="color:red;cursor: pointer" onclick="remove_server(\'\#= id \#\')"></a></div>'
        }
    ]
};

var select_server_grid = set_table("#server_list", grid_option);

if (servers_selected.length > 0) {
    $("#server_p").removeClass("display_none");
    select_server_grid.dataSource.read();
}


function remove_server(id) {
    var server = {};
    for (var i = 0; i < servers_selected.length; i++) {
        if (servers_selected[i].id == id)
            server = servers_selected[i]
    }
    servers_selected.splice(servers_selected.indexOf(server), 1);
    select_server_grid.dataSource.read();
}

function add_server() {
    servers_selected.splice(0, servers_selected.length);
    var treeObj = $.fn.zTree.getZTreeObj("tree_sys");
    var select_servers = treeObj.getCheckedNodes(true);
    for (var i = 0; i < select_servers.length; i++) {
        if (select_servers[i].type == "IP") {
            servers_selected.push(select_servers[i]);
        }
    }
    select_server_grid.dataSource.read();
}

var tree_server = [];

var tree_option = {
    data: {
        key: {
            name: "name",
            checked: "checked"
        }
    },
    check: {enable: true},
    onClick: function (event, treeId, treeNode) {
        get_children(treeNode);
    },
    onCheck: function (event, treeId, treeNode) {
        get_all_children(treeNode);
    },
    enableAsyn: false
};

var app_id_list = "";

function useradd() {
    if(servers_selected.length ==0){
    app_alert("请选择服务器！");
    return;
    }
    var d = dialog({
        width: 500,
        title: '新建用户',
        content: $("#alertDiv")[0],
        okValue: '提交',
        ok: function () {
            data_info = {
                linux_username: $('#linux_username').val(),
                linux_pwd: $('#linux_pwd').val(),
                servers: servers_selected,
            }
            var data = JSON.stringify(data_info);
            show_loading();
            $.post(site_url + "useradd/", {"data": data}, function (res) {
                close_loading();
                if (res.is_success == "one") {
                    app_none_modal_alert(res.message);

                }
                else if (res.is_success == "two") {
                    app_alert(res.message);
                }
                else {
                    app_alert(res.message);
                }
            }).error(function(error) {
                if (error.status == 403) {
                    app_alert("没有权限")
                }
                else {
                    alert(error)
                }

            })},
        cancelValue: '取消',
        cancel: function () {

        }

    })
    d.showModal()
}

function confirm() {
    var ipList = "";
    // var os_type=$('input:radio[name="os_select"]:checked').val();
    // var password_1 = $("#password_1").val();
    // var password = $("#password").val();
    // if (!os_type) {
    // app_alert("请确认系统类型！");
    // return;
    // }
    // if (!password || !password_1) {
    // app_alert("密码不能为空！");
    // return;
    // }
    // if (password.length > 79 || password_1.length >79) {
    // app_alert("密码位数不能大于79")
    // return
    // }
    // if (password != password_1) {
    // app_alert("两次密码必须相同！");
    // return;
    // }
    if(servers_selected.length ==0){
    app_alert("请选择服务器！");
    return;
    }
    var data_info = {
        // password: password,
        servers: servers_selected,
        // os_type:os_type
    };

    var data = JSON.stringify(data_info);
    show_loading();
    $.post(site_url + "fast_execute_script/", {"data": data}, function (res) {
            close_loading();
            if (res.is_success == "one") {
                app_none_modal_alert(res.message);
                $.each(res.query_list, function (index, val) {
                    $("#user_data").append("<tr>" +
                        "<td>" + index + "</td>" +
                        "<td>" + val.ip + "</td>" +
                        "<td>" + val.user_name + "</td>" +
                        "<td>" + val.user_home + "</td>" +
                        "<td>" + val.user_shell + "</td>" +
                        "<td><button type='button' onclick=\"change_password('" + val.ip + "," + val.user_name + "," + val.source + "," + val.app_id +
                        "')\" class=\"btn btn-xs btn-inverse\" title=\"修改密码\">\n" +
                        "                        <i class=\"glyphicon glyphicon-edit\"></i>\n" +
                        "                    </button>\n" +
                        "                    <button type='button' onclick=\"userdel('" + val.ip + "," + val.user_name + "," + val.source + "," + val.app_id +
                        "')\" class=\"btn btn-xs btn-inverse\" title=\"删除用户\">\n" +
                        "                        <i class=\"glyphicon glyphicon-remove\"></i>\n" +
                        "                    </button></td>" +
                        "</tr>");

                })
                // $("#user_data").html(
                //     for (var i=0; i<res.query_list.length; i++) {
                //         document.write("333");
                //     }
                // );
            }
            else if (res.is_success == "two") {
                app_alert(res.message);
            }
            else {
                app_alert(res.message);
            }
        }
    ).error(function(error) {
        close_loading();
        if (error.status == 403) {
            app_alert("没有权限")
        }
        else {
            alert(error)
        }

    })

}

function test() {
    alert("test");

}


function userdel(args) {
    data_info = {
        ip: args.split(",")[0],
        username: args.split(",")[1],
        source: args.split(",")[2],
        app_id: args.split(",")[3],
    };
    //     data_info = {
    //     linux_username: $('#linux_username').val(),
    //     linux_pwd: $('#linux_pwd').val(),
    //     servers: servers_selected,
    // }
    var data = JSON.stringify(data_info);
    show_loading();
    $.post(site_url + "userdel/", {"data": data}, function (res) {
                close_loading();
                if (res.is_success == "one") {
                    app_alert(res.message);

                }
                else if (res.is_success == "two") {
                    app_alert(res.message);
                }
                else {
                    app_alert(res.message);
                }
            }).error(function(error) {
                if (error.status == 403) {
                    app_alert("没有权限")
                }
                else {
                    alert(error.status)
                }
            })
}


function change_password(args) {
    var d = dialog({
        width: 500,
        title: '修改密码',
        content: $("#changePwdDiv")[0],
        okValue: '提交',
        ok: function () {
            data_info = {
                password: $('#linux_new_pwd').val(),
                ip: args.split(",")[0],
                username: args.split(",")[1],
                source: args.split(",")[2],
                app_id: args.split(",")[3],
            }
            var data = JSON.stringify(data_info);
            show_loading();
            $.post(site_url + "change_password/", {"data": data}, function (res) {
                close_loading();
                if (res.is_success == "one") {
                    app_none_modal_alert(res.message);

                }
                else if (res.is_success == "two") {
                    app_alert(res.message);
                }
                else {
                    app_alert(res.message);
                }
            }).error(function(error) {
                if (error.status == 403) {
                    app_alert("没有权限")
                }
                else {
                    alert(error)
                }

            })},
        cancelValue: '取消',
        cancel: function () {

        }

    })
    d.showModal()
}


function cancel() {
    window.location.reload()
}



function select_server() {
    var d = dialog({
        width: 350,
        title: '选择服务器',
        content: '<div style="width:100%;overflow-y: auto">\
    <div style="width:100%;overflow-y: auto">\
        <div style="width:100%;height:100%;">\
            <div style="width:100%;height:35px;">\
                <input type="text" class="form-control" id="sys_ip" style="width:70.5%;float: left;">\
                <button class="king-btn-demo king-btn king-primary" style="float:left;margin-left: 5px; " onclick="search_business();"><span style="line-height:0.2;" class="fa fa-search"></span>&nbsp;查找</button>\
            </div>\
            <div style="width: 100%; height: 100%;  padding-top: 5px;" id="sys_tree_div">\
                <div style="border:1px solid #ddd;overflow-y: auto;min-height: 300px" id="tree_sys" class="ztree"></div>\
            </div>\
        </div>\
    </div>\
</div>',
        onshow: function (arguments) {
            search_business();
        },
        okValue: '确定',
        ok: function () {
            show_loading();
            servers_selected.splice(0, servers_selected.length);
            app_id_list = "";
            var treeObj = $.fn.zTree.getZTreeObj("tree_sys");
            var select_servers = treeObj.getCheckedNodes(true);
            for (var i = 0; i < select_servers.length; i++) {
                if (select_servers[i].type == "IP") {
                    //servers_selected.push(select_servers[i]);
                    servers_selected.push({
                        ip:select_servers[i].ip,
                        app_id:select_servers[i].app_id,
                        source:select_servers[i].source,
                        id:select_servers[i].id
                    })
                }
                // if (select_servers[i].type == "first") {
                //     app_id_list += select_servers[i].id + ";";
                // }
            }
            $("#server_p").removeClass("display_none");
            select_server_grid.dataSource.read();
            close_loading();
        },
        cancelValue: '取消',
        cancel: function () {
            // do something
        }
    });
    d.showModal();
}

var tree_server = [];

var tree_option = {
    data: {
        key: {
            name: "name",
            checked: "checked"
        }
    },
    check: {enable: true},
    onClick: function (event, treeId, treeNode) {
        get_children(treeNode);
    },
    onCheck: function (event, treeId, treeNode) {
        get_all_children(treeNode);
    },
    enableAsyn: false
};

function search_business() {
    // var system_type = $("#sys_select .select2_box").select2("val");
    var sys_ip = $("#sys_ip").val();
    show_loading();
    if (sys_ip == "")
        get_business();
    else
        get_server_by_ip(sys_ip);
}

function get_server_by_ip(ip) {
    $.post(site_url + "get_sys_tree_by_ip/", {
        ip: ip
    }, function (res) {
        close_loading();
        if (!res.is_success) {
            app_alert(res.message);
            return;
        }
        tree_server = res.data;
        $("#sys_tree_div").children().remove();
        $("#sys_tree_div").append('<div style="border:1px solid #ddd;overflow-y: auto;min-height: 300px" id="tree_sys" class="ztree"></div>');
        set_ztree(tree_option, "#tree_sys", tree_server);
    })
}

function get_business() {
    $.post(site_url + "get_sys_tree/", {}, function (res) {
        close_loading();
        if (!res.result) {
            app_alert(res.message);
            return;
        }
        tree_server = res.data;
        $("#sys_tree_div").children().remove();
        $("#sys_tree_div").append('<div style="border:1px solid #ddd;overflow-y: auto;min-height: 300px" id="tree_sys" class="ztree"></div>');
        set_ztree(tree_option, "#tree_sys", tree_server);
    })
}

function get_all_children(treeNode) {
    if (treeNode.is_open) {
        if (treeNode.type == "first") {
            if (treeNode.children_add)
                return;
            else {
                $.post(site_url + "get_module_server/", {
                    "id": treeNode.id
                }, function (res) {
                    close_loading();
                    var treeObj = $.fn.zTree.getZTreeObj("tree_sys");
                    treeObj.removeChildNodes(treeNode);
                    for (var i = 0; i < res.data.length; i++) {
                        treeObj.addNodes(treeNode, res.data[i]);
                    }
                    treeNode.is_open = true;
                    treeNode.children_add = true;
                })
            }
        }
        else {
            return;
        }
    }
    show_loading();
    if (treeNode.type == "first") {
        $.post(site_url + "get_module_server/", {
            "id": treeNode.id
        }, function (res) {
            close_loading();
            var treeObj = $.fn.zTree.getZTreeObj("tree_sys");
            treeObj.removeChildNodes(treeNode);
            for (var i = 0; i < res.data.length; i++) {
                treeObj.addNodes(treeNode, res.data[i]);
            }
            treeNode.is_open = true;
            treeNode.children_add = true;
        })
    }
    else if (treeNode.type == "second") {
        var parent_id = treeNode.getParentNode().id;
        $.post(site_url + "get_server_by_module_id/", {"id": treeNode.id, "parent_id": parent_id}, function (res) {
            close_loading();
            var treeObj = $.fn.zTree.getZTreeObj("tree_sys");
            for (var i = 0; i < res.data.length; i++) {
                res.data[i].checked = true;
                res.data[i].icon = static_url+"img/server_icon.png";
                treeObj.addNodes(treeNode, res.data[i]);
            }
            treeNode.is_open = true;
        })
    }
    else {
        close_loading();
        return;
    }
}

function get_children(treeNode) {
    if (treeNode.is_open)
        return;
    show_loading();

    if (treeNode.type == "first") {
        $.post(site_url + "get_module_by_app_id/", {"id": treeNode.id}, function (res) {
            close_loading();
            var treeObj = $.fn.zTree.getZTreeObj("tree_sys");
            for (var i = 0; i < res.data.length; i++) {
                // res.data[i].checked = is_checked;
                treeObj.addNodes(treeNode, res.data[i]);
            }
            treeNode.is_open = true;
        })
    }
    else if (treeNode.type == "second") {
        var parent_id = treeNode.getParentNode().id;
        $.post(site_url + "get_server_by_module_id/", {"id": treeNode.id, "parent_id": parent_id}, function (res) {
            close_loading();
            var treeObj = $.fn.zTree.getZTreeObj("tree_sys");
            for (var i = 0; i < res.data.length; i++) {
                //res.data[i].checked = is_checked;
                res.data[i].icon = static_url+"img/server_icon.png";
                treeObj.addNodes(treeNode, res.data[i]);
            }
            treeNode.is_open = true;
        })
    }
    else {
        close_loading();
        return;
    }
}
