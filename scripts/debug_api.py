import sys
import json
from project_config import save_tmp
from jadx_client import get_from_jadx, get_all_classes, search_classes_by_keyword


print("Testing search API...")
result = search_classes_by_keyword("Cipher", search_in="code", count=10)

print("Search result type:", type(result))
print("Search result:", json.dumps(result, indent=2, ensure_ascii=False)[:1000])
print()

print("Getting all classes...")
all_classes = get_all_classes()
if all_classes:
    print("All classes type:", type(all_classes))
    print("All classes keys:", all_classes.keys() if isinstance(all_classes, dict) else "N/A")
    classes_list = all_classes.get("classes", [])
    print(f"Found {len(classes_list)} classes")
    print("First 10 classes:")
    for cls in classes_list[:10]:
        print(f"  - {type(cls)}: {cls}")
    
    all_classes_file = save_tmp("all_classes.json", json.dumps(all_classes, indent=2, ensure_ascii=False))
    print(f"\n数据已保存到: {all_classes_file}")
