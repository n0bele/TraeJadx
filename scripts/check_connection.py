import httpx
import time

print("检查 JADX 插件连接...")
for i in range(3):
    try:
        r = httpx.get('http://127.0.0.1:8650/health', timeout=3)
        print(f"尝试 {i+1}: 状态码 {r.status_code}")
        print(f"响应: {r.text}")
        if r.status_code == 200:
            print('✅ JADX 插件已连接！')
            break
    except Exception as e:
        print(f"尝试 {i+1}: 连接失败 - {e}")
        time.sleep(1)
