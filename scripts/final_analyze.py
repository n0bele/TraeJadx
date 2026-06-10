import sys
import json
from collections import defaultdict
from project_config import save_tmp, save_result, tmp_path, result_path
from jadx_client import (
    get_from_jadx,
    get_all_classes,
    search_classes_by_keyword,
    get_package_tree,
    get_class_source
)


print("=" * 70)
print("APK Security Analysis - Encryption & Communication")
print("=" * 70)
print()

print("[Step 1] Loading all classes...")
all_classes_data = get_all_classes()
all_classes = []
if all_classes_data:
    all_classes = all_classes_data.get("classes", [])
    print(f"Total classes (first 100): {len(all_classes)}")
    save_tmp("all_classes.json", json.dumps(all_classes_data, indent=2, ensure_ascii=False))
print()

print("[Step 2] Searching for cryptography-related code...")
crypto_keywords = [
    "Cipher", "AES", "RSA", "DES", "3DES", "MD5", "SHA", "HMAC",
    "SecretKey", "KeyGenerator", "KeyPair", "KeyStore",
    "encrypt", "decrypt", "cipher", "signature", "certificate"
]

crypto_classes = defaultdict(list)

for keyword in crypto_keywords:
    found = search_classes_by_keyword(keyword, count=25)
    if found and found.get("classes"):
        crypto_classes[keyword] = [cls.get("name") if isinstance(cls, dict) else cls for cls in found.get("classes", [])]
        print(f"  {keyword}: {len(crypto_classes[keyword])} classes found")

all_crypto_classes = set()
for classes in crypto_classes.values():
    all_crypto_classes.update(classes)

print()
print(f"[+] Total crypto-related classes found: {len(all_crypto_classes)}")
if all_crypto_classes:
    print("\nTop crypto classes:")
    for cls in sorted(all_crypto_classes)[:30]:
        print(f"  - {cls}")
print()

print("[Step 3] Searching for network communication code...")
network_keywords = [
    "OkHttp", "Retrofit", "HttpURLConnection", "HttpClient",
    "Request", "Response", "Interceptor", "WebSocket",
    "http://", "https://", "URL", "URI"
]

network_classes = defaultdict(list)

for keyword in network_keywords:
    found = search_classes_by_keyword(keyword, count=25)
    if found and found.get("classes"):
        network_classes[keyword] = [cls.get("name") if isinstance(cls, dict) else cls for cls in found.get("classes", [])]
        print(f"  {keyword}: {len(network_classes[keyword])} classes found")

all_network_classes = set()
for classes in network_classes.values():
    all_network_classes.update(classes)

print()
print(f"[+] Total network-related classes found: {len(all_network_classes)}")
if all_network_classes:
    print("\nTop network classes:")
    for cls in sorted(all_network_classes)[:30]:
        print(f"  - {cls}")
print()

print("[Step 4] Searching for potential hardcoded secrets...")
secret_keywords = [
    "key", "secret", "password", "token", "api", "API_KEY", 
    "PRIVATE_KEY", "PUBLIC_KEY", "AES_KEY", "RSA_KEY"
]

secret_classes = defaultdict(list)

for keyword in secret_keywords:
    found = search_classes_by_keyword(keyword, count=20)
    if found and found.get("classes"):
        secret_classes[keyword] = [cls.get("name") if isinstance(cls, dict) else cls for cls in found.get("classes", [])]
        print(f"  {keyword}: {len(secret_classes[keyword])} classes found")

all_secret_classes = set()
for classes in secret_classes.values():
    all_secret_classes.update(classes)

print()
print(f"[+] Classes with potential secrets: {len(all_secret_classes)}")
if all_secret_classes:
    print("\nTop classes:")
    for cls in sorted(all_secret_classes)[:20]:
        print(f"  - {cls}")
print()

print("[Step 5] Analyzing package structure...")
package_tree = get_package_tree()
if package_tree:
    packages = package_tree.get("packages", [])
    app_packages = [p for p in packages if not p.get("is_likely_library", False)]
    print(f"Total packages: {package_tree.get('total_packages', 0)}")
    print(f"App packages (non-library): {len(app_packages)}")
    print("\nMain app packages:")
    for pkg in sorted(app_packages, key=lambda x: x.get("class_count", 0), reverse=True)[:15]:
        print(f"  - {pkg.get('name')}: {pkg.get('class_count')} classes")
    save_tmp("package_tree.json", json.dumps(package_tree, indent=2, ensure_ascii=False))
print()

overlap_classes = all_crypto_classes & all_network_classes
print(f"[Step 6] Critical classes with both crypto and network: {len(overlap_classes)}")

if overlap_classes:
    print("\nCritical classes (crypto + network):")
    for cls in sorted(overlap_classes)[:10]:
        print(f"  - {cls}")

print()
print("=" * 70)
print("Analysis Summary")
print("=" * 70)
print()
print("Key Findings:")
print(f"  - Crypto classes: {len(all_crypto_classes)}")
print(f"  - Network classes: {len(all_network_classes)}") 
print(f"  - Potential secret classes: {len(all_secret_classes)}")
print(f"  - Critical overlap classes: {len(overlap_classes)}")
print()

results = {
    "crypto_classes": sorted(all_crypto_classes),
    "network_classes": sorted(all_network_classes),
    "secret_classes": sorted(all_secret_classes),
    "overlap_classes": sorted(overlap_classes),
    "crypto_by_keyword": dict(crypto_classes),
    "network_by_keyword": dict(network_classes)
}

result_file = save_result("security-analysis-results.json", json.dumps(results, indent=2, ensure_ascii=False))
crypto_file = save_tmp("crypto_classes_list.json", json.dumps(sorted(all_crypto_classes), indent=2, ensure_ascii=False))
network_file = save_tmp("login_classes_list.json", json.dumps(sorted(all_network_classes), indent=2, ensure_ascii=False))
secret_file = save_tmp("login_sources.json", json.dumps(sorted(all_secret_classes), indent=2, ensure_ascii=False))
crypto_sources_file = save_tmp("crypto_sources.json", json.dumps(dict(crypto_classes), indent=2, ensure_ascii=False))

print(f"Results saved to: {result_file}")
print(f"Crypto list saved to: {crypto_file}")
print(f"Network list saved to: {network_file}")
print(f"Secret list saved to: {secret_file}")
print()
print("[Step 7] Getting source code for critical classes...")

key_classes_to_check = list(overlap_classes)[:3] + list(all_crypto_classes)[:3] + list(all_secret_classes)[:3]

cls_sources = {}
for cls_name in key_classes_to_check:
    try:
        source_data = get_class_source(cls_name)
        if source_data:
            print(f"\n--- {cls_name} ---")
            content = source_data.get("source", "")
            print(content[:1000] + "..." if len(content) > 1000 else content)
            cls_sources[cls_name] = content
    except Exception as e:
        print(f"Error getting {cls_name}: {e}")

if cls_sources:
    critical_file = save_result("critical-classes-source.json", json.dumps(cls_sources, indent=2, ensure_ascii=False))
    print(f"\nCritical class sources saved to: {critical_file}")
