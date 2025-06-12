[app]
title = KivyApp
package.name = kivyapp
package.domain = org.mimaling
source.dir = .
source.include_exts = py,mp3,kv,png,jpg,atlas
source.include_dirs = 开始语,指令,结束语
version = 0.1
requirements = python3,kivy==2.3.0,pygame==2.5.2
orientation = portrait
fullscreen = 1

# 项目入口文件
main.py = main_kivy.py

# 权限（如需访问文件、录音等可添加更多）
android.permissions = INTERNET

[buildozer]
log_level = 2
