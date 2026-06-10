import httpx
import json
from project_config import save_tmp, tmp_path
from jadx_client import JADX_URL, get_all_resource_file_names


r = httpx.get(f"{JADX_URL}/all-resource-file-names", params={"count": 200}, timeout=60)
print(f"状态码: {r.status_code}")
text = r.text
print(text[:12000])

if r.status_code == 200:
    try:
        data = json.loads(text)
        resource_file = save_tmp("all_resources.json", json.dumps(data, indent=2, ensure_ascii=False))
        print(f"\n资源文件列表已保存到: {resource_file}")
    except Exception:
        pass
