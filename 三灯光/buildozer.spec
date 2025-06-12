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

# 包含的音频文件夹及格式
android.presplash = 
android.icon = 

# 权限
android.permissions = INTERNET

# 日志
log_level = 2

[buildozer]
log_level = 2

[android]
# 额外依赖设置
android.requirements = kivy,pygame

# 如果有特殊 Java 依赖，请按需补充
# android.add_jars =

# 设置 Python 版本（可选）
# python3 = True

# 其它设置按需补充
