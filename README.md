---
title: 【ST插件】文件头生成
tags: 
  - SublimeText
  - opensource
---

## 简介|Introductions

<div>
    <img flex="left" src="https://img.shields.io/badge/python-%3E%3D3.8.0-3776AB"/>
    <img flex="left" src="https://img.shields.io/badge/Sublime%20Text-FF9800?style=flat&logo=Sublime%20Text&logoColor=white"/>
    <img flex="left" src="https://img.shields.io/github/license/caoxiemeihao/electron-vite-vue?style=flat"/>
</div>
同类插件 sublimeText 已经有，但很久没更新，而且功能配置比较复杂，配置起来有点没弄明白，所以特意重复造个轮子给自己的团队使用。

> - 本插件为团队内部打造使用，不对外更新负责，
> - 2023年了，前端建议采用**VSCode**。

![fileheader](/screenshot/sublimeTextPlugs/cps-fileheader/fileheader.gif)

![fileheader](http://localhost:45462/image/fileheader.gif)



## 功能|Feature

- 快速插入文件头部信息
- 根据后缀名关联模板
- 一种后缀名可关联多个模板（vue2 和 vue3）

- `Alt  + f`在当前文件插入文件头，支持自定义模板和对应格式



## 安装|Install

```bash
# 打开 SublimeText3的插件目录，并在该目录下打开shell
菜单栏 > Preferences > Browse Packages...

# 在插件目录运行shell，下载插件
# gitee
git clone --depth=1 git@gitee.com:Capsion-ST-PLugins/fileheader.git cps_fileheader
# or github
git clone --depth=1 git@github.com:Capsion-ST-PLugins/fileheader.git cps_fileheader

# 重启ST
ctrl + s
```



## 配置文件|Configure

### **快捷键**

- `Packages/User/Default.sublime-keymap`

```js
[
  {
    "keys": ["alt+f"],
    "command": "cps_add_file_header"
  },
]
```

### **插件配置**

- `Packages/User/cps.sublime-settings`

```js
{
  "fileheader":{
    "update_header_on_openfile": false, // 打开文件的时候是否检查需要更新头部信息
    "update_header_on_savefile": false, // 保存时是否更新头部信息

    // 后缀名关联模板文件，不通过语法识别
    "template": {
      //模版插件目录/fileheader/header/*.tmpl
      // "文件格式":"对应的 xxxx.tmpl 文件",
      // 支持多个.tmpl文件
      ".bat": "Batch File",
      ".pug": "pug",
      ".js": "JavaScript",
      ".json": "JavaScript",
      ".cjs": "JavaScript", //comment.js 文件
      ".mjs": "JavaScript", //ES6文件
      ".ts": "JavaScript",
      ".css": "CSS",
      ".scss": "SCSS",
      ".less": "less",
      ".stylus": "styl",
      ".styl": "styl",
      ".vue": ["vue", "vue2", "vue3", "vue2-ts", "vue3-setup"],
      ".py": "Python"
    },

    // 模板变量
    "header_info": {
      "author": "CPS",
      "email": "373704015@qq.com",
      "create_time": "", // 输入一个时间格式 默认: "%Y-%m-%d %H:%M:%S" | "%Y-%m-%d" | "%H:%M:%S"
      "last_modified_by": "CPS", // 输入一个时间格式 默认: "%Y-%m-%d %H:%M:%S" | "%Y-%m-%d" | "%H:%M:%S"
      "last_modified_time": "", // 输入一个时间格式 默认: "%Y-%m-%d %H:%M:%S" | "%Y-%m-%d" | "%H:%M:%S"
      "project_name": "",
      "file_path": "",
      "file_name": "",
      "自定义": "{{自定义}}" //自定义要替换的信息，模板文件中使用 "{{变量名称}}" 替代即可
    }
  },
}
```



## 项目架构|Tree

```basic
DIR:cps-fileheader                # 
   |-- .sublime/                  # 
   |   |-- Default.sublime-keymap # 
   |   `-- Context.sublime-menu   # 
   |-- core/                      # 「core」核心代码
   |   `-- utils.py               # 
   |-- headerTmpl/                # 「headerTmpl」默认的模板文件
   |   |-- vue3.tmpl              # 
   |   |-- vue3-setup.tmpl        # 
   |   |-- vue2.tmpl              # 
   |   |-- vue2-ts.tmpl           # 
   |   |-- vue.tmpl               # 
   |   |-- styl.tmpl              # 
   |   |-- SCSS.tmpl              # 
   |   |-- Python.tmpl            # 
   |   |-- pug.tmpl               # 
   |   |-- less.tmpl              # 
   |   |-- JavaScript.tmpl        # 
   |   |-- HTML.tmpl              # 
   |   |-- CSS.tmpl               # 
   |   `-- Batch File.tmpl        # 
   |-- screenshot/                # 「screenshot」
   |   `-- fileheader1.gif        # 
   |-- README.md                  # 
   |-- main.py                    # 插件入口
   `-- .python-version            # 

```



## 联系方式|Contact

- **373704015 (qq、wechat、email)**
