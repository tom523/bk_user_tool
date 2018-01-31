# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云(BlueKing) available.
Copyright (C) 2017 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
"""

from blueking.component.shortcuts import get_client_by_request
from common.mymako import render_mako_context, render_json
from conf.default import APP_ID, APP_TOKEN, BK_PAAS_HOST
import base64
from blueking.component.shortcuts import get_client_by_user
from common.log import logger
import logging
import sys

formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
console_handler = logging.StreamHandler(sys.stdout)
console_handler.formatter = formatter
logger.addHandler(console_handler)
logger.setLevel(logging.DEBUG)


def home(request):
    """
    首页
    """
    return render_mako_context(request, '/home_application/home.html')

def dev_guide(request):
    """
    开发指引
    """
    return render_mako_context(request, '/home_application/dev_guide.html')


def contactus(request):
    """
    联系我们
    """
    return render_mako_context(request, '/home_application/contact.html')


def get_sys_tree(request):
    try:
        client = get_client_by_request(request)
        kwargs = {}
        result = client.cc.get_app_by_user(kwargs)
        if result["result"]:
            datas = result["data"]
            app_list = [{"name": data["ApplicationName"], "id": data["ApplicationID"],
                         "checked": False, "isParent": False, "type": "first",
                         "children_add": False, "is_open": False} for data in datas if data["ApplicationID"] != "1"]

        return render_json({"result": True, "data": app_list})
    except Exception, e:
        return render_json({"result": False, "error": e})


def get_module_by_appid(request):
    applicationID = request.POST.get("id")
    client = get_client_by_request(request)
    kwargs = {
        "app_id": applicationID
    }
    result = client.cc.get_app_host_list(kwargs)
    if result["result"]:
        return_data = []
        template_data = result["data"]
        module_ids = []
        for data in template_data:
            if data["ModuleID"] not in module_ids:
                module_ids.append(data["ModuleID"])
                return_data.append({"name": data["ModuleName"], "id": data["ModuleID"], "checked": False,
                                    "type": "second", "is_open": False, "isParent": False})
    else:
        return_data = []
    return render_json({"result": True, "data": return_data})


def get_server_by_module_id(request):
    client = get_client_by_request(request)
    app_id = request.POST.get("parent_id")
    module_id = request.POST.get("id")
    kwargs = {
        "app_id": app_id,
        "module_id": module_id
    }
    result = client.cc.get_module_host_list(kwargs)
    if result["result"]:
        datas = result["data"]
    else:
        datas = []
    return_data = [
        {"name": "[" + data["InnerIP"] + "] " + data["HostName"], "is_open": True, "isParent": False,
         "id": str(data["InnerIP"]).replace('.', '_'), "checked": False, "ip": data["InnerIP"], "type": "IP",
         "icon": "../../static/images/server_icon.png", "source": data["Source"], "app_id": data["ApplicationID"]}
        for data in datas]
    logger.debug(return_data)
    return render_json({"result": True, "data": return_data})


def get_user_name(request):
    return request.user.username


def useradd(request):
    try:
        user_name = get_user_name(request)
        logger.debug(eval(request.POST.get("data")))
        data = eval(request.POST.get("data"))
        linux_username = data["linux_username"]
        linux_pwd = data["linux_pwd"]
        servers = data["servers"]
        account = "root"
        script_content = "useradd %s && echo %s | passwd %s --stdin" % (linux_username,linux_pwd,linux_username)
        logger.debug(script_content)
        check_apps = set_check_apps(servers)
        import sys
        reload(sys)
        sys.setdefaultencoding('utf-8')
        for check_app in check_apps:
            kwargs = {
                "app_code": APP_ID,
                "app_secret": APP_TOKEN,
                "app_id": check_app["app_id"],
                "username": user_name,
                "content": base64.encodestring(script_content),
                "ip_list": check_app["ip_list"],
                "type": 1,
                "account": account,
                "script_param": ""
            }
            logger.debug(kwargs)
            client = get_client_by_user(request)
            result = client.job.fast_execute_script(kwargs)
            logger.debug(result)
            if result["result"]:
                script_result = get_task_ip_log(client, result["data"]["taskInstanceId"], user_name)
                logger.debug(script_result)
                ips_fail = ''
                ips_sucess = ''
                for i in script_result:
                    if i["result"] == True:
                        ips_sucess = i["ips"]
                    elif i["result"] == False:
                        ips_fail = i["ips"]
                logger.debug(ips_sucess)
                success_list = []
                for item in ips_sucess:

                    success_list.append(item[0])

                success_list = ",".join(success_list)
                # fail_list = ",".join(ips_fail)
                operator = get_user_name(request)
                sucess_num = str(len(ips_sucess))
                fail_num = str(len(ips_fail))
                if len(ips_fail) == 0:
                    operated_detail = sucess_num + u"台服务器新建用户成功"
                    message = sucess_num + u"台服务器新建用户成功:" + success_list
                    # insert_log(operator, sucess_list, fail_list,operated_detail)
                    return render_json({'is_success': "one", "message": message})
                else:
                    if len(ips_sucess) == 0:
                        operated_detail = fail_num + u"台服务器密码修改失败"
                        message = fail_num + u"台服务器密码修改失败:"
                    else:
                        operated_detail = sucess_num + u"台服务器修改密码成功" + ";" + fail_num + u"台服务器修改密码失败"
                        message = sucess_num + u"台服务器修改密码成功:" + success_list + "<br>" + fail_num + u"台服务器修改密码失败:"
                    # insert_log(operator, sucess_list, fail_list, operated_detail)
                    return render_json({'is_success': "two", "message": message})
    except Exception, e:
        logger.error(e.message)
        return render_json({"is_success": "three", "message": e.message})


def change_password(request):
    try:
        user_name = get_user_name(request)
        logger.debug(eval(request.POST.get("data")))
        data = eval(request.POST.get("data"))
        logger.debug(data)
        username = data["username"]
        ip = data["ip"]
        source = data["source"]
        app_id = data["app_id"]
        password = data["password"]
        ip_list = [{"ip": ip, "source": source}, ]
        # servers = data["servers"]
        account = "root"
        script_content = "echo %s | passwd %s --stdin " % (password, username)
        logger.debug(script_content)
        # check_apps = set_check_apps(servers)
        import sys
        reload(sys)
        sys.setdefaultencoding('utf-8')
        # for check_app in check_apps:
        kwargs = {
            "app_code": APP_ID,
            "app_secret": APP_TOKEN,
            "app_id": app_id,
            "username": user_name,
            "content": base64.encodestring(script_content),
            "ip_list": ip_list,
            "type": 1,
            "account": account,
            "script_param": ""
        }
        logger.debug(kwargs)
        client = get_client_by_user(request)
        result = client.job.fast_execute_script(kwargs)
        logger.debug(result)
        if result["result"]:
            script_result = get_task_ip_log(client, result["data"]["taskInstanceId"], user_name)
            logger.debug(script_result)
            ips_fail = ''
            ips_sucess = ''
            for i in script_result:
                if i["result"] == True:
                    ips_sucess = i["ips"]
                elif i["result"] == False:
                    ips_fail = i["ips"]
            logger.debug(ips_sucess)
            success_list = []
            for item in ips_sucess:

                success_list.append(item[0])

            success_list = ",".join(success_list)
            # fail_list = ",".join(ips_fail)
            operator = get_user_name(request)
            sucess_num = str(len(ips_sucess))
            fail_num = str(len(ips_fail))
            if len(ips_fail) == 0:
                operated_detail = sucess_num + u"台服务器修改用户密码成功"
                message = sucess_num + u"台服务器修改用户密码成功:" + success_list
                # insert_log(operator, sucess_list, fail_list,operated_detail)
                return render_json({'is_success': "one", "message": message})
            else:
                if len(ips_sucess) == 0:
                    operated_detail = fail_num + u"台服务器密码修改失败"
                    message = fail_num + u"台服务器密码修改失败:"
                else:
                    operated_detail = sucess_num + u"台服务器修改密码成功" + ";" + fail_num + u"台服务器修改密码失败"
                    message = sucess_num + u"台服务器修改密码成功:" + success_list + "<br>" + fail_num + u"台服务器修改密码失败:"
                # insert_log(operator, sucess_list, fail_list, operated_detail)
                return render_json({'is_success': "two", "message": message})
    except Exception, e:
        logger.error(e.message)
        return render_json({"is_success": "three", "message": e.message})


def userdel(request):
    try:
        user_name = get_user_name(request)
        logger.debug(eval(request.POST.get("data")))
        data = eval(request.POST.get("data"))
        logger.debug(data)
        username = data["username"]
        ip = data["ip"]
        source = data["source"]
        app_id = data["app_id"]
        password = data["password"]
        ip_list = [{"ip": ip, "source": source}, ]
        # servers = data["servers"]
        account = "root"
        script_content = "userdel %s " % (username,)
        logger.debug(script_content)
        # check_apps = set_check_apps(servers)
        import sys
        reload(sys)
        sys.setdefaultencoding('utf-8')
        # for check_app in check_apps:
        kwargs = {
            "app_code": APP_ID,
            "app_secret": APP_TOKEN,
            "app_id": app_id,
            "username": user_name,
            "content": base64.encodestring(script_content),
            "ip_list": ip_list,
            "type": 1,
            "account": account,
            "script_param": ""
        }
        logger.debug(kwargs)
        client = get_client_by_user(request)
        result = client.job.fast_execute_script(kwargs)
        logger.debug(result)
        if result["result"]:
            script_result = get_task_ip_log(client, result["data"]["taskInstanceId"], user_name)
            logger.debug(script_result)
            ips_fail = ''
            ips_sucess = ''
            for i in script_result:
                if i["result"] == True:
                    ips_sucess = i["ips"]
                elif i["result"] == False:
                    ips_fail = i["ips"]
            logger.debug(ips_sucess)
            success_list = []
            for item in ips_sucess:

                success_list.append(item[0])

            success_list = ",".join(success_list)
            # fail_list = ",".join(ips_fail)
            operator = get_user_name(request)
            sucess_num = str(len(ips_sucess))
            fail_num = str(len(ips_fail))
            if len(ips_fail) == 0:
                operated_detail = sucess_num + u"台服务器删除用户成功"
                message = sucess_num + u"台服务器删除用户成功:" + success_list
                # insert_log(operator, sucess_list, fail_list,operated_detail)
                return render_json({'is_success': "one", "message": message})
            else:
                if len(ips_sucess) == 0:
                    operated_detail = fail_num + u"台服务器密码修改失败"
                    message = fail_num + u"台服务器密码修改失败:"
                else:
                    operated_detail = sucess_num + u"台服务器修改密码成功" + ";" + fail_num + u"台服务器修改密码失败"
                    message = sucess_num + u"台服务器修改密码成功:" + success_list + "<br>" + fail_num + u"台服务器修改密码失败:"
                # insert_log(operator, sucess_list, fail_list, operated_detail)
                return render_json({'is_success': "two", "message": message})
    except Exception, e:
        logger.error(e.message)
        return render_json({"is_success": "three", "message": e.message})


def fast_execute_script(request):
    try:
        user_name = get_user_name(request)
        data = eval(request.POST.get("data"))
        servers = data["servers"]
        logger.debug(servers)
        # password = data["password"]
        # os_type = data["os_type"]
        # if os_type == "L":
        #     script_content = "echo %s |passwd --stdin root" % password
        #     type = "1"
        #     account = "root"
        # elif os_type == "W":
        #     script_content = "net user administrator %s" % password
        #     type = "2"
        #     account = "administrator"
        account = "root"
        script_content = "cat /etc/passwd"
        check_apps = set_check_apps(servers)
        logger.debug(check_apps)
        import sys
        reload(sys)
        sys.setdefaultencoding('utf-8')
        for check_app in check_apps:
            kwargs = {
                "app_code": APP_ID,
                "app_secret": APP_TOKEN,
                "app_id": check_app["app_id"],
                "username": user_name,
                "content": base64.encodestring(script_content),
                "ip_list": check_app["ip_list"],
                "type": 1,
                "account": account,
                "script_param": ""
            }
            logger.debug(kwargs)
            client = get_client_by_user(request)
            result = client.job.fast_execute_script(kwargs)
            logger.debug(result)
            if result["result"]:
                script_result = get_task_ip_log(client, result["data"]["taskInstanceId"], user_name)
                logger.debug(script_result)
                ips_fail = ''
                ips_sucess = ''
                for i in script_result:
                    if i["result"] == True:
                        ips_sucess = i["ips"]
                    elif i["result"] == False:
                        ips_fail = i["ips"]
                logger.debug(ips_sucess)
                success_list = []
                query_list = []
                for item in ips_sucess:

                    success_list.append(item[0])

                    user_list = item[1].split("\n")
                    user_list.remove("")
                    for user in user_list:
                        user_detail = user.split(":")
                        if int(user_detail[2]) >= 1000:
                            user_result = {}
                            user_result["ip"] = item[0]
                            # 能过IP查找app_id,source
                            for server in servers:
                                if server['ip'] == user_result['ip']:
                                    user_result['app_id'] = server['app_id']
                                    user_result['source'] = server['source']
                            logger.debug("查询到用户：" + user_detail[0])
                            user_result['user_name'] = user_detail[0]
                            user_result['user_home'] = user_detail[5]
                            user_result['user_shell'] = user_detail[6]
                            logger.debug(u"添加用户到list：" + str(user_result))
                            query_list.append(user_result)
                logger.debug(query_list)
                success_list = ",".join(success_list)
                # fail_list = ",".join(ips_fail)
                operator = get_user_name(request)
                sucess_num = str(len(ips_sucess))
                fail_num = str(len(ips_fail))
                if len(ips_fail) == 0:
                    operated_detail = sucess_num+u"台服务器查询成功"
                    message = sucess_num+u"台服务器查询成功:" + success_list
                    # insert_log(operator, sucess_list, fail_list,operated_detail)
                    return render_json({'is_success': "one","message": message, "query_list": query_list})
                else:
                    if len(ips_sucess) == 0:
                        operated_detail = fail_num + u"台服务器密码修改失败"
                        message = fail_num + u"台服务器密码修改失败:"
                    else:
                        operated_detail = sucess_num + u"台服务器修改密码成功"  +";" + fail_num + u"台服务器修改密码失败"
                        message = sucess_num + u"台服务器修改密码成功:" + success_list + "<br>" + fail_num + u"台服务器修改密码失败:"
                    # insert_log(operator, sucess_list, fail_list, operated_detail)
                    return render_json({'is_success': "two","message": message})
    except Exception, e:
        logger.error(e.message)
        return render_json({"is_success": "three", "message": e.message})


def set_check_apps(servers):
    server_list = servers
    app_id_list = []
    for i in server_list:
        if i["app_id"] not in app_id_list:
            app_id_list.append(i["app_id"])
    return_data = []
    for u in app_id_list:
        ip_list = []
        for i in server_list:
            if u == i["app_id"]:
                ip_list.append({"ip": i["ip"], "source": i["source"]})
        return_data.append({"app_id":u,"ip_list":ip_list})
    return return_data


def get_task_ip_log(client, task_instance_id, user_name):
    kwargs = {
        "app_code": APP_ID,
        "app_secret": APP_TOKEN,
        "username": user_name,
        "task_instance_id": task_instance_id
    }
    result = client.job.get_task_ip_log(kwargs)
    logger.debug(result["data"][0])
    if result["result"]:
        if result["data"][0]["isFinished"]:
            # return_result = [{"result":False,"ips":''},{"result":True,"ips":''}]
            return_result=[]
            log_content = []
            logger.debug(result["data"][0]["stepAnalyseResult"])
            logger.debug(result["data"][0]["stepAnalyseResult"][0]["resultType"])
            logger.debug(len(result["data"][0]["stepAnalyseResult"]))
            for i in result["data"][0]["stepAnalyseResult"]:
                if i["resultType"] != 9:
                    logger.error(u"脚本执行失败，错误码如下：")
                    logger.error(i["resultType"])
                    logger.error(i["resultTypeText"])
                    return_result.append({"result":False,"ips":[u["ip"] for u in i["ipLogContent"]]})
                else:
                    log_content += i["ipLogContent"]
                    return_result.append({"result": True, "ips": [(u["ip"], u['logContent']) for u in i["ipLogContent"]]})
                    logger.debug(return_result)
            return return_result
        else:
            import time
            time.sleep(10)
            return get_task_ip_log(client, task_instance_id, user_name)
    else:
        logger.error(result["message"])
        return ""


def search_log_detail():
    pass


