import httpx
import json
from project_config import tmp_path
from jadx_client import JADX_URL, check_health, get_all_classes


test_endpoints = [
    "health",
    "all-classes",
    "package-tree", 
    "main-activity",
    "search-progress"
]

print("测试 JADX 插件 API 端点...")
print("=" * 50)

for endpoint in test_endpoints:
    try:
        response = httpx.get(f"{JADX_URL}/{endpoint}", timeout=5)
        print(f"✅ {endpoint}: 状态码 {response.status_code}")
        if response.text and len(response.text) < 200:
            print(f"   响应: {response.text}")
    except Exception as e:
        print(f"❌ {endpoint}: 错误 - {e}")

print()
print("尝试获取所有类...")
try:
    data = get_all_classes()
    if data:
        classes = data.get("classes", [])
        print(f"找到 {len(classes)} 个类")
        if classes:
            print("\n前 20 个类:")
            for cls in classes[:20]:
                print(f"  - {cls}")
except Exception as e:
    print(f"错误: {e}")
