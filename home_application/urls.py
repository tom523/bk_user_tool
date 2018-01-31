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

from django.conf.urls import patterns

urlpatterns = patterns(
    'home_application.views',
    (r'^$', 'home'),
    (r'^dev-guide/$', 'dev_guide'),
    (r'^contactus/$', 'contactus'),

    # 任务执行
    (r'^fast_execute_script/$', 'fast_execute_script'),
    (r'^useradd/$', 'useradd'),
    (r'^userdel/$', 'userdel'),
    (r'^change_password/$', 'change_password'),
    # (r'^get_log_list/$', 'get_log_list'),
    # (r'^search_business/$', 'search_business'),
    # (r'^get_server_list/$', 'get_server_list'),
    # (r'^modify_pass_diff/$', 'modify_pass_diff'),
    # (r'^search_log_detail/$', 'search_log_detail'),

    (r'^get_sys_tree/', 'get_sys_tree'),
    (r'^get_module_by_app_id/', 'get_module_by_appid'),
    (r'^get_server_by_module_id/', 'get_server_by_module_id'),
)
