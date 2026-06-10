import sys
import json
from collections import defaultdict
from project_config import save_tmp, save_result, result_path
from jadx_client import get_from_jadx, search_classes_by_keyword, get_package_tree


print("=" * 70)
print("APK Security Analysis - Encryption & Communication")
print("=" * 70)
print()

print("[Step 1] Loading all classes...")
all_classes_data = get_from_jadx("all-classes")
all_classes = []
if all_classes_data:
    all_classes = all_classes_data.get("classes", [])
    print(f"Total classes: {len(all_classes)}")
    save_tmp("all_classes.json", json.dumps(all_classes_data, indent=2, ensure_ascii=False))
else:
    print("Failed to get classes")
print()

print("[Step 2] Searching for cryptography-related code...")
crypto_keywords = [
    "Cipher", "AES", "RSA", "DES", "3DES", "MD5", "SHA", "HMAC",
    "SecretKey", "KeyGenerator", "KeyPair", "KeyStore",
    "encrypt", "decrypt", "cipher", "signature", "certificate"
]

crypto_classes = defaultdict(list)

for keyword in crypto_keywords:
    result = search_classes_by_keyword(keyword, search_in="code", count=30)
    if result and result.get("classes"):
        found = result.get("classes", [])
        crypto_classes[keyword].extend([cls.get("name") if isinstance(cls, dict) else cls for cls in found])
        print(f"  {keyword}: {len(found)} classes found")

all_crypto_classes = set()
for classes in crypto_classes.values():
    all_crypto_classes.update(classes)

print()
print(f"[+] Total crypto-related classes found: {len(all_crypto_classes)}")
if all_crypto_classes:
    print("\nTop crypto classes:")
    for cls in list(all_crypto_classes)[:30]:
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
    result = search_classes_by_keyword(keyword, search_in="code", count=30)
    if result and result.get("classes"):
        found = result.get("classes", [])
        network_classes[keyword].extend([cls.get("name") if isinstance(cls, dict) else cls for cls in found])
        print(f"  {keyword}: {len(found)} classes found")

all_network_classes = set()
for classes in network_classes.values():
    all_network_classes.update(classes)

print()
print(f"[+] Total network-related classes found: {len(all_network_classes)}")
if all_network_classes:
    print("\nTop network classes:")
    for cls in list(all_network_classes)[:30]:
        print(f"  - {cls}")
print()

print("[Step 4] Searching for potential hardcoded secrets...")
secret_keywords = [
    "key", "secret", "password", "token", "api", "API_KEY", 
    "PRIVATE_KEY", "PUBLIC_KEY", "AES_KEY", "RSA_KEY"
]

secret_classes = defaultdict(list)

for keyword in secret_keywords:
    result = search_classes_by_keyword(keyword, search_in="code", count=20)
    if result and result.get("classes"):
        found = result.get("classes", [])
        secret_classes[keyword].extend([cls.get("name") if isinstance(cls, dict) else cls for cls in found])
        print(f"  {keyword}: {len(found)} classes found")

all_secret_classes = set()
for classes in secret_classes.values():
    all_secret_classes.update(classes)

print()
print(f"[+] Classes with potential secrets: {len(all_secret_classes)}")
if all_secret_classes:
    print("\nTop classes:")
    for cls in list(all_secret_classes)[:20]:
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

print("[Step 6] Analyzing sample classes...")

overlap_classes = all_crypto_classes & all_network_classes
print(f"Classes with both crypto and network: {len(overlap_classes)}")

if overlap_classes:
    print("\nCritical classes (crypto + network):")
    for cls in list(overlap_classes)[:10]:
        print(f"  - {cls}")

print()
print("=" * 70)
print("Analysis Summary")
print("=" * 70)
print()
print("Key Findings:")
print(f"  - Total classes: {len(all_classes)}")
print(f"  - Crypto classes: {len(all_crypto_classes)}")
print(f"  - Network classes: {len(all_network_classes)}") 
print(f"  - Potential secret classes: {len(all_secret_classes)}")
print()

results = {
    "crypto_classes": list(all_crypto_classes),
    "network_classes": list(all_network_classes),
    "secret_classes": list(all_secret_classes),
    "overlap_classes": list(overlap_classes),
    "crypto_by_keyword": dict(crypto_classes),
    "network_by_keyword": dict(network_classes)
}

result_file = save_result("security-analysis-results.json", json.dumps(results, indent=2, ensure_ascii=False))
crypto_file = save_tmp("crypto_classes_list.json", json.dumps(list(all_crypto_classes), indent=2, ensure_ascii=False))
network_file = save_tmp("login_classes_list.json", json.dumps(list(all_network_classes), indent=2, ensure_ascii=False))

print(f"Results saved to: {result_file}")
print(f"Crypto list saved to: {crypto_file}")
print(f"Network list saved to: {network_file}")
print()
print("Next steps:")
print("1. Examine the critical classes with both crypto and network code")
print("2. Check for hardcoded keys in the secret-related classes")
print("3. Analyze SSL/TLS implementation")
print("4. Look for insecure random number generation")
print("5. Check WebView configurations if present")
