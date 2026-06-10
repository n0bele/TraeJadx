import json
from collections import defaultdict
from project_config import save_tmp, save_result, tmp_path, result_path
from jadx_client import (
    get_from_jadx,
    get_android_manifest,
    get_package_tree,
    search_classes_by_keyword,
    get_strings,
    get_main_activity
)


print("=" * 60)
print("APK 安全分析 - 通信加解密检查")
print("=" * 60)
print()

manifest = get_android_manifest()
if manifest:
    print("[1/6] 获取 AndroidManifest.xml...")
    if isinstance(manifest, dict) and manifest.get("content"):
        print("✅ AndroidManifest.xml 获取成功")
        manifest_content = manifest.get("content", "")
        manifest_file = save_tmp("android_manifest.xml", manifest_content)
        print(f"已保存到: {manifest_file}")
    else:
        manifest_content = str(manifest)
    print("AndroidManifest.xml 预览:")
    print(manifest_content[:500] + "..." if len(manifest_content) > 500 else manifest_content)
else:
    print("❌ 获取 AndroidManifest 失败")
print()

print("[2/6] 获取包结构...")
package_tree = get_package_tree()
if package_tree:
    print(f"✅ 发现 {package_tree.get('total_classes', 0)} 个类，{package_tree.get('total_packages', 0)} 个包")
    packages = package_tree.get("packages", [])
    print("\n主要包结构:")
    for pkg in packages[:10]:
        print(f"  - {pkg.get('name')}: {pkg.get('class_count')} 个类")
    package_tree_file = save_tmp("package_tree.json", json.dumps(package_tree, indent=2, ensure_ascii=False))
    print(f"\n包结构已保存到: {package_tree_file}")
else:
    print("❌ 获取包结构失败")
print()

print("[3/6] 搜索加解密相关代码...")
crypto_keywords = [
    "Cipher", "AES", "RSA", "DES", "3DES", "MD5", "SHA", "HMAC", 
    "SecretKey", "KeyGenerator", "KeyPair", "KeyStore",
    "encrypt", "decrypt", "cipher", "signature", "certificate"
]

found_crypto_classes = []
crypto_results = {}
for keyword in crypto_keywords[:5]:
    result = search_classes_by_keyword(keyword, search_in="code", count=20)
    if result and result.get("classes"):
        print(f"  搜索 '{keyword}': 找到 {len(result.get('classes', []))} 个相关类")
        found_crypto_classes.extend(result.get("classes", []))
        crypto_results[keyword] = result

if found_crypto_classes:
    print(f"\n✅ 找到 {len(found_crypto_classes)} 个与加解密相关的类")
    print("\n前 10 个相关类:")
    seen = set()
    for cls in found_crypto_classes[:20]:
        name = cls.get("name", "") if isinstance(cls, dict) else cls
        if name and name not in seen:
            seen.add(name)
            print(f"  - {name}")
    crypto_classes_file = save_tmp("crypto_classes_list.json", json.dumps(list(seen), indent=2, ensure_ascii=False))
    crypto_sources_file = save_tmp("crypto_sources.json", json.dumps(crypto_results, indent=2, ensure_ascii=False))
    print(f"\n加密类列表已保存到: {crypto_classes_file}")
    print(f"加密源数据已保存到: {crypto_sources_file}")
else:
    print("❌ 未找到明显的加解密相关类")
print()

print("[4/6] 搜索网络通信相关代码...")
network_keywords = [
    "OkHttp", "Retrofit", "HttpURLConnection", "HttpClient", 
    "Request", "Response", "Interceptor", "WebSocket",
    "http://", "https://", "URL", "URI"
]

found_network_classes = []
for keyword in network_keywords[:5]:
    result = search_classes_by_keyword(keyword, search_in="code", count=20)
    if result and result.get("classes"):
        print(f"  搜索 '{keyword}': 找到 {len(result.get('classes', []))} 个相关类")
        found_network_classes.extend(result.get("classes", []))

if found_network_classes:
    print(f"\n✅ 找到 {len(found_network_classes)} 个与网络相关的类")
    print("\n前 10 个相关类:")
    seen = set()
    for cls in found_network_classes[:20]:
        name = cls.get("name", "") if isinstance(cls, dict) else cls
        if name and name not in seen:
            seen.add(name)
            print(f"  - {name}")
else:
    print("❌ 未找到明显的网络相关类")
print()

print("[5/6] 检查 strings.xml 中的敏感信息...")
strings_result = get_strings(offset=0, count=50)
if strings_result:
    strings = strings_result.get("strings", [])
    print(f"✅ 获取到 {len(strings)} 个字符串")
    sensitive_patterns = ["key", "secret", "password", "token", "api", "http", "https"]
    found_sensitive = []
    for s in strings:
        s_lower = s.lower()
        for pat in sensitive_patterns:
            if pat in s_lower:
                found_sensitive.append(s)
                break
    if found_sensitive:
        print(f"\n⚠️  发现 {len(found_sensitive)} 个可能的敏感字符串:")
        for s in found_sensitive[:20]:
            print(f"  - {s[:80]}{'...' if len(s) > 80 else ''}")
        strings_file = save_tmp("all_sources.txt", "\n".join(strings))
        print(f"\n所有字符串已保存到: {strings_file}")
    else:
        print("\n未发现明显的敏感字符串")
else:
    print("❌ 获取 strings.xml 失败")
print()

print("[6/6] 获取主 Activity...")
main_activity = get_main_activity()
if main_activity:
    print(f"✅ 主 Activity: {main_activity.get('class_name', 'unknown')}")
    main_activity_file = save_tmp("main_activity.json", json.dumps(main_activity, indent=2, ensure_ascii=False))
    print(f"主 Activity 数据已保存到: {main_activity_file}")
else:
    print("❌ 获取主 Activity 失败")

print()
print("=" * 60)
print("分析完成！")
print("=" * 60)
print()
print("临时文件保存在 tmp/ 目录")
print("结果文件保存在 result/ 目录")
print()
print("下一步:")
print("1. 查看发现的加密和网络相关类的详细代码")
print("2. 检查是否有硬编码的密钥")
print("3. 分析 SSL/TLS 配置")
print("4. 查看 WebView 的安全配置")
