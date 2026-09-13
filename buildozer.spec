[app]
title = Matrix
package.name = matrix
package.domain = com.yuvraj.matrix
source.dir =.
source.include_exts = py,png,jpg,kv,atlas,json,txt
version = 0.1
requirements = python3,kivy
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2

# (important) android api
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
