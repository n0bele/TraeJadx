import sys
import json
import re
from project_config import save_tmp, save_result, tmp_path, result_path
from jadx_client import (
    search_classes_by_keyword,
    get_class_source,
    get_strings,
    get_all_classes
)

# AES相关关键词搜索
AES_KEYWORDS = [
    "AES", "SecretKey", "KeyGenerator", "KeySpec",
    "SecretKeySpec", "Cipher.getInstance", "AES/ECB", "AES/CBC"
]

# 可能的密钥模式
KEY_PATTERNS = [
    r'([a-fA-F0-9]{32})',           # 16字节密钥（32个hex字符）
    r'([a-fA-F0-9]{48})',           # 24字节密钥
    r'([a-fA-F0-9]{64})',           # 32字节密钥
    r'["\']([^\'"]{16,64})["\']',   # 字符串常量
    r'byte\[\]\s*(\w+)\s*=\s*\{',   # 字节数组定义
    r'(\w+)\s*=\s*new byte\['       # 新字节数组
]

def find_potential_keys():
    print("=" * 80)
    print("🔍 AES 密钥查找工具")
    print("=" * 80)
    print()

    all_classes = []
    try:
        data = get_all_classes()
        if data:
            all_classes = data.get("classes", [])
        print(f"✅ 获取到 {len(all_classes)} 个类")
    except Exception as e:
        print(f"❌ 获取类列表失败: {e}")
    print()

    crypto_classes = []
    for keyword in AES_KEYWORDS[:5]:
        print(f"🔍 搜索关键词: {keyword}")
        result = search_classes_by_keyword(keyword, search_in="code", count=50)
        if result and result.get("classes"):
            found = [cls.get("name") if isinstance(cls, dict) else cls for cls in result.get("classes", [])]
            crypto_classes.extend(found)
            print(f"   找到 {len(found)} 个相关类")
    crypto_classes = list(set(crypto_classes))
    print(f"\n📦 总共找到 {len(crypto_classes)} 个与加密相关的类")

    potential_keys = []
    string_results = []

    print("\n" + "=" * 80)
    print("📝 分析字符串资源")
    print("=" * 80)
    try:
        strings_data = get_strings(offset=0, count=500)
        if strings_data:
            strings = strings_data.get("strings", [])
            print(f"✅ 获取到 {len(strings)} 个字符串")
            for s in strings:
                for pattern in KEY_PATTERNS[:3]:
                    matches = re.findall(pattern, s)
                    if matches:
                        for match in matches:
                            string_results.append({
                                "type": "hex_string",
                                "value": match,
                                "context": s[:100]
                            })
            if string_results:
                print(f"\n⚠️  发现 {len(string_results)} 个可能的十六进制密钥:")
                for r in string_results[:20]:
                    print(f"   - {r['value']}")
    except Exception as e:
        print(f"❌ 获取字符串失败: {e}")

    print("\n" + "=" * 80)
    print("🔬 分析加密类源代码")
    print("=" * 80)

    analyzed_classes = []
    for cls_name in crypto_classes[:30]:
        try:
            source_data = get_class_source(cls_name)
            if source_data and source_data.get("source"):
                source = source_data.get("source")
                analyzed_classes.append({
                    "class_name": cls_name,
                    "source": source
                })
                print(f"\n📄 分析类: {cls_name}")

                for pattern in KEY_PATTERNS:
                    matches = re.findall(pattern, source)
                    if matches:
                        print(f"   ⚠️  匹配模式 '{pattern[:50]}...':")
                        for match in matches[:5]:
                            print(f"      - {str(match)[:100]}")
                            potential_keys.append({
                                "class": cls_name,
                                "pattern": pattern,
                                "match": str(match)
                            })

                if len(analyzed_classes) % 5 == 0:
                    print(f"\n   (已分析 {len(analyzed_classes)} 个类，继续...)")

        except Exception as e:
            print(f"❌ 分析 {cls_name} 失败: {e}")

    print("\n" + "=" * 80)
    print("📊 分析结果汇总")
    print("=" * 80)

    print(f"\n加密相关类数量: {len(crypto_classes)}")
    print(f"可能的密钥线索: {len(potential_keys)}")
    print(f"字符串资源中的可能密钥: {len(string_results)}")

    results = {
        "crypto_classes": crypto_classes,
        "potential_keys": potential_keys,
        "string_results": string_results,
        "analyzed_classes": analyzed_classes
    }

    result_file = save_result("aes_key_search_results.json", json.dumps(results, indent=2, ensure_ascii=False))
    print(f"\n💾 详细结果已保存到: {result_file}")

    if crypto_classes:
        print("\n" + "=" * 80)
        print("🎯 建议重点查看的类（按可能包含密钥的优先级）:")
        print("=" * 80)
        for cls in crypto_classes[:20]:
            print(f"  - {cls}")

    print("\n" + "=" * 80)
    print("💡 提示:")
    print("  1. 查看上面列出的加密相关类的源代码")
    print("  2. 重点搜索 'SecretKey', 'SecretKeySpec', 'byte[]'")
    print("  3. 检查硬编码的十六进制字符串 (32/48/64位)")
    print("  4. 查看详细的结果文件: result/aes_key_search_results.json")
    print("=" * 80)

if __name__ == "__main__":
    find_potential_keys()
