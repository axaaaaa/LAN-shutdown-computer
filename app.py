from flask import Flask, render_template, request, jsonify, send_file
import os
import ctypes
import win32gui
import win32con
import time
import psutil
from datetime import datetime, timedelta
from mss import mss
from PIL import Image

app = Flask(__name__)

def get_uptime():
    try:
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot_time
        days = uptime.days
        hours = uptime.seconds // 3600
        minutes = (uptime.seconds % 3600) // 60
        seconds = uptime.seconds % 60
        return {
            "days": days,
            "hours": hours,
            "minutes": minutes,
            "seconds": seconds
        }
    except Exception as e:
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_uptime', methods=['GET'])
def uptime():
    try:
        uptime_data = get_uptime()
        if uptime_data:
            return jsonify({
                "status": "success",
                "data": uptime_data
            })
        return jsonify({
            "status": "error",
            "message": "无法获取运行时间"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })

@app.route('/shutdown', methods=['POST'])
def shutdown():
    try:
        os.system('shutdown /s /t 1')
        return jsonify({"status": "success", "message": "关机命令已执行"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/timed_shutdown', methods=['POST'])
def timed_shutdown():
    try:
        minutes = request.json.get('minutes', 0)
        if not isinstance(minutes, int) or minutes < 0:
            return jsonify({"status": "error", "message": "请输入有效的分钟数"})
        seconds = minutes * 60
        os.system(f'shutdown /s /t {seconds}')
        return jsonify({"status": "success", "message": f"{minutes}分钟后将关机"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/cancel_shutdown', methods=['POST'])
def cancel_shutdown():
    try:
        os.system('shutdown /a')
        return jsonify({"status": "success", "message": "已取消定时关机"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/restart', methods=['POST'])
def restart():
    try:
        os.system('shutdown /r /t 1')
        return jsonify({"status": "success", "message": "重启命令已执行"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/logout', methods=['POST'])
def logout():
    try:
        os.system('shutdown /l')
        return jsonify({"status": "success", "message": "注销命令已执行"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/lock', methods=['POST'])
def lock():
    try:
        ctypes.windll.user32.LockWorkStation()
        return jsonify({"status": "success", "message": "锁定屏幕命令已执行"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/screen_off', methods=['POST'])
def screen_off():
    try:
        win32gui.SendMessage(win32con.HWND_BROADCAST, win32con.WM_SYSCOMMAND, win32con.SC_MONITORPOWER, 2)
        return jsonify({"status": "success", "message": "关闭屏幕命令已执行"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/screen_on', methods=['POST'])
def screen_on():
    try:
        win32gui.SendMessage(win32con.HWND_BROADCAST, win32con.WM_SYSCOMMAND, win32con.SC_MONITORPOWER, -1)
        return jsonify({"status": "success", "message": "开启屏幕命令已执行"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/screenshot')
def take_screenshot():
    try:
        # 创建截图文件夹（如果不存在）
        screenshot_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'screenshots')
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)

        # 使用mss进行截图
        with mss() as sct:
            # 获取主显示器的截图
            monitor = sct.monitors[1]  # 主显示器
            screenshot = sct.grab(monitor)
            
            # 将截图转换为PIL Image
            img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
            
            # 生成文件名（使用时间戳）
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'screenshot_{timestamp}.png'
            filepath = os.path.join(screenshot_dir, filename)
            
            # 保存图片
            img.save(filepath)
            
            # 返回图片文件
            return send_file(filepath, mimetype='image/png')
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    # 获取本机IP地址
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(f"请访问: http://{local_ip}:5000")
    app.run(host='0.0.0.0', port=5000)
