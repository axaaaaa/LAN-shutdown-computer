# 局域网关机系统

![界面预览](1.png)

这是一个基于 Flask 开发的局域网电脑控制系统，允许用户通过网页界面远程控制电脑的关机、重启、锁屏等操作。

## 功能特点

- 响应式设计：支持在各种设备上使用
- 实时显示系统运行时间
- 远程截图功能
- 丰富的控制功能：
  - 关机
  - 重启
  - 注销
  - 锁定屏幕
  - 关闭/开启显示器
  - 定时关机
  - 取消定时关机

## 系统要求

- Python 3.6+
- Windows 操作系统

## 依赖包

```
flask
psutil
mss
Pillow
pywin32
```

## 安装步骤

1. 克隆或下载本项目到本地
2. 安装所需依赖：
   ```
   pip install flask psutil mss Pillow pywin32
   ```
3. 运行 `start.bat` 或直接运行 `python app.py`

## 使用方法

💡 你可以使用手机直接访问显示的地址来控制电脑，支持在同一局域网内使用任何带浏览器的设备（手机、平板、其他电脑等）进行控制。

1. 运行程序后，系统会自动显示访问地址（例如：http://192.168.1.100:5000）
2. 在同一局域网内的其他设备上，通过浏览器访问该地址
3. 在网页界面上可以进行以下操作：
   - 点击"关机"按钮立即关机
   - 点击"重启"按钮重启电脑
   - 点击"注销"按钮注销当前用户
   - 点击"锁定屏幕"按钮锁定电脑
   - 点击"关闭显示器"按钮关闭显示器
   - 点击"开启显示器"按钮开启显示器
   - 使用定时关机功能，设置指定分钟数后关机
   - 点击"取消定时关机"取消已设置的定时关机
   - 点击"截图"按钮获取当前屏幕截图

## 技术实现

- 后端：Flask (Python)
- 前端：HTML5 + CSS3 + JavaScript
- 系统操作：
  - `psutil`: 获取系统运行时间
  - `ctypes`: 实现锁屏功能
  - `win32gui`: 控制显示器
  - `mss`: 实现截图功能

## 注意事项

1. 本程序需要在 Windows 系统上运行
2. 使用时确保运行程序的电脑和控制设备在同一局域网内
3. 部分功能可能需要管理员权限
4. 建议在可信任的网络环境中使用

## 文件结构

```
局域网关机/
├── app.py              # 主程序文件
├── templates/          # 模板文件夹
│   └── index.html     # 网页界面
├── screenshots/        # 截图保存文件夹
└── start.bat  # 快捷启动文件
