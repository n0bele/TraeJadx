import sys
import json
from project_config import save_tmp, result_path
from jadx_client import get_from_jadx, check_health, get_all_classes, get_package_tree


print("Testing JADX plugin API endpoints...")
print("=" * 50)

if not check_health():
    print("警告: JADX 插件可能未连接")
print()

print("Trying to get all classes...")
try:
    data = get_all_classes()
    if data:
        classes = data.get("classes", [])
        print(f"Found {len(classes)} classes")
        if classes:
            print("\nFirst 20 classes:")
            for cls in classes[:20]:
                print(f"  - {cls}")
        all_classes_file = save_tmp("all_classes.json", json.dumps(data, indent=2, ensure_ascii=False))
        print(f"\n所有类数据已保存到: {all_classes_file}")
except Exception as e:
    print(f"Error: {e}")

print()
print("Trying package tree...")
try:
    data = get_package_tree()
    if data:
        print(data)
        package_tree_file = save_tmp("package_tree.json", json.dumps(data, indent=2, ensure_ascii=False))
        print(f"\n包结构数据已保存到: {package_tree_file}")
except Exception as e:
    print(f"Error: {e}")
