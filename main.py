# -*- coding: utf-8 -*-
#
# @Author: CPS
# @email: 373704015@qq.com
# @Date:
# @Last Modified by: CPS
# @Last Modified time: 2021-08-05 11:34:45.888952
# @file_path "Z:\CPS\IDE\SublimeText\sublime_text_4113.21_win64_test\Data\Packages\testt_fileheader"
# @Filename "file_header.py"
# @Description: 功能描述
#

import sublime
import sublime_plugin
import datetime
import os, shutil

from .core import utils

TMPL_PATH = ""
PLUGIN_NAME = __package__

SETTINGS = {}
SETTING_KEY = "fileheader"
SETTING_FILE = "cps.sublime-settings"

# 原生文件头
DEFAULT_TMPL_FLODER = os.path.join(sublime.packages_path(), __package__, "headerTmpl")
# 用户自定义文件
TMPL_FLODER = os.path.join(sublime.packages_path(), "User", "cpsHeaderTmpl")


def plugin_loaded():
    global SETTINGS, SETTING_KEY, SETTING_FILE

    # 创建默认的的模板
    if not os.path.exists(TMPL_FLODER):
        shutil.copytree(DEFAULT_TMPL_FLODER, TMPL_FLODER)

    SETTINGS = SettingManager(SETTING_KEY, SETTING_FILE)


class SettingManager:
    def __init__(self, setting_key: str, default_settings: str):
        self.setting_key = setting_key
        self.default_settings = default_settings
        self.default_settings_path = os.path.join(
            sublime.packages_path(), "cps-plugins", ".sublime", default_settings
        )

        self.data = {}

        sublime.set_timeout_async(self.plugin_loaded_async)

    def __getitem__(self, key: str, default={}):
        if key in self.data:
            return self.data.get(key, default)
        else:
            return {}

    def get(self, key: str, default={}):
        return self.__getitem__(key, default)

    def plugin_loaded_async(self):
        """
        @Description 监听用户配置文件
        """
        with open(self.default_settings_path, "r", encoding="utf8") as f:
            self.data = sublime.decode_value(f.read()).get(self.setting_key, {})

        # 读取现有配置
        user_settings = sublime.load_settings(self.default_settings)
        # 添加配置更新事件
        user_settings.add_on_change(self.default_settings, self._on_settings_change)
        # 将最新的配置更新到内部的data，最终以data为准
        utils.recursive_update(self.data, user_settings.to_dict()[self.setting_key])

    def _on_settings_change(self):
        new_settings = sublime.load_settings(self.default_settings).get(
            self.setting_key, {}
        )

        utils.recursive_update(self.data, new_settings)

        return self


class CpsAddFileHeaderCommand(sublime_plugin.TextCommand):
    def run(self, edit, user_select_index: int = -1):
        file_name = self.view.file_name()
        print("file_name: ", file_name)
        dir_path = os.path.dirname(file_name)
        print("dir_path: ", dir_path)
        try:
            tmp_file = self.get_tmpl_file(file_name)
            if len(tmp_file) > 1:
                if user_select_index > -1:
                    tmp_file = tmp_file[list(tmp_file.keys())[int(user_select_index)]]

                else:
                    # tmpl文件存在多个时，调用选择框给予选择
                    sublime.active_window().show_quick_panel(
                        items=tmp_file.keys(),
                        on_select=self.get_user_select_syntax,
                        placeholder="检测到该格式存在多个模板文件：",
                    )
                    return
            else:
                tmp_file = tmp_file[list(tmp_file.keys())[0]]

            tmpl_info = self.get_header_info(file_name)
            print("tmpl_info: ", tmpl_info)
            header_info = self.render_header_info_by_tmpl(tmp_file, tmpl_info)
            print("header_info: ", header_info)

            if header_info:
                self.insert_info(edit, header_info)

        except Exception as e:
            print("cps AddFileHeaderCommand，发生错误: ", e)

    # 用户选择后的回调，将用户所选择的语法传给函数
    def get_user_select_syntax(self, index: int) -> None:
        """
        @Description 弹出选择框让用户选择tmpl文件

        - param index :{int} 用户选择的文件，如果是-1，则表示没有选择，不作任何动作
        """
        if index != -1:
            sublime.active_window().run_command(
                "cps_add_file_header", {"user_select_index": index}
            )

    def insert_info(self, edit, header_info):
        cursor_offset = self.view.sel()[0].end()
        res = self.view.insert(edit, 0, header_info)

        if res:
            self.view.show_at_center(cursor_offset)

    def get_header_info(self, filename: str):
        global SETTINGS
        info = SETTINGS.get("header_info", {})

        # 文件字符串少于2的话,当作是一个新文件,添加创建时间
        if self.view.sel()[0].end() <= 1:
            info = self.on_add_file(info)
        info = self.add_file_base_info(info)

        return info

    def get_tmpl_file(self, filename: str) -> dict:
        global SETTINGS, TMPL_FLODER
        template = SETTINGS.get("template", {})

        # 检查当前后缀名是否存在对应的 tmpl 模板文件
        _, ext = os.path.splitext(filename)
        res = {}
        if ext.lower() in template.keys():
            if isinstance(template[ext], list):
                # 当前格式存在多个.tmpl文件，弹出选择框给予选择
                for tmpl_name in template[ext]:
                    res[tmpl_name] = os.path.join(TMPL_FLODER, tmpl_name) + ".tmpl"
            else:
                res[ext] = os.path.join(TMPL_FLODER, template[ext]) + ".tmpl"

        return res

    def render_header_info_by_tmpl(self, tmpl_file, info):
        if os.path.exists(tmpl_file):
            # 读取tmpl文件
            res = ""
            with open(tmpl_file, "r", encoding="utf8") as tmpl:
                for each in tmpl.readlines():
                    for key, val in info.items():
                        each = each.replace("{{" + key + "}}", val)
                    res += each
            return res

    def on_add_file(self, info):
        info["create_time"] = self.get_now(info["create_time"])
        return info

    def add_file_base_info(self, info):
        """
        @Description {description}

        - param info :{param} {description}

        @returns `{}` {description}

        """
        info["last_modified_time"] = self.get_now(info["last_modified_time"])
        info["file_path"] = os.path.dirname(self.view.file_name())
        basename = os.path.basename(self.view.file_name())

        if basename.startswith("index"):
            # 如果文件是 index.xxxx, 就把文件夹名作为文件名
            info["file_name"] = os.path.basename(info["file_path"])
        else:
            info["file_name"] = basename

        return info

    def get_now(self, fmat=r"%Y-%m-%d %H:%M:%S"):
        return datetime.datetime.now().__format__(fmat)
