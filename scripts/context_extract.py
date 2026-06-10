import httpx
import json
from project_config import save_tmp, tmp_path
from jadx_client import JADX_URL, get_class_source


requests = {
  "world.letsgo.booster.android.application.c": [(150,175),(200,220),(270,315),(570,595)],
  "world.letsgo.booster.android.proxy.ProxyService": [(320,335),(680,700),(980,1000),(1160,1228),(2485,2535)],
  "com.stripe.android.stripe3ds2.security.DefaultMessageTransformer": [(1,220)],
  "com.stripe.android.stripe3ds2.security.TransactionEncrypter": [(68,110)],
  "anet.channel.security.b": [(45,115)],
  "io.ably.lib.util.Crypto": [(35,120),(184,260)]
}

extracted_data = {}

for cls, ranges in requests.items():
    r = httpx.get(f"{JADX_URL}/class-source", params={"class_name": cls}, timeout=60)
    lines = r.text.splitlines()
    print("="*100)
    print(cls)
    
    class_extracts = []
    for start, end in ranges:
        print(f"--- lines {start}-{end} ---")
        extract = []
        for idx in range(start, min(end, len(lines))+1):
            line = f"{idx}: {lines[idx-1]}"
            print(line)
            extract.append(line)
        print()
        class_extracts.append({
            "range": (start, end),
            "lines": extract
        })
    
    extracted_data[cls] = {
        "full_source": r.text,
        "extracts": class_extracts
    }

if extracted_data:
    output_file = save_tmp("extracted_context.json", json.dumps(extracted_data, indent=2, ensure_ascii=False))
    print(f"提取的数据已保存到: {output_file}")
