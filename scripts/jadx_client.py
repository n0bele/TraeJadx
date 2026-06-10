import httpx
import json
import sys


if sys.version_info >= (3, 7):
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')


JADX_URL = "http://127.0.0.1:8650"


def get_from_jadx(endpoint, params=None, timeout=60):
    try:
        response = httpx.get(f"{JADX_URL}/{endpoint}", params=params, timeout=timeout)
        response.raise_for_status()
        return response.json() if response.text else None
    except Exception as e:
        print(f"请求 {endpoint} 失败: {e}")
        return None


def post_to_jadx(endpoint, params=None):
    try:
        response = httpx.post(f"{JADX_URL}/{endpoint}", params=params, timeout=60)
        response.raise_for_status()
        return response.json() if response.text else None
    except Exception as e:
        print(f"POST 请求 {endpoint} 失败: {e}")
        return None


def check_health():
    try:
        response = httpx.get(f"{JADX_URL}/health", timeout=5)
        return response.status_code == 200
    except Exception:
        return False


def get_all_classes(offset=0, count=0):
    return get_from_jadx("all-classes", {"offset": offset, "count": count})


def get_class_source(class_name):
    return get_from_jadx("class-source", {"class_name": class_name})


def get_package_tree():
    return get_from_jadx("package-tree")


def get_main_activity():
    return get_from_jadx("main-activity")


def get_android_manifest():
    return get_from_jadx("android-manifest")


def search_classes_by_keyword(search_term, package="", search_in="code", offset=0, count=20):
    return get_from_jadx("search-classes-by-keyword", {
        "search_term": search_term,
        "package": package,
        "search_in": search_in,
        "offset": offset,
        "count": count
    })


def get_strings(offset=0, count=0):
    return get_from_jadx("strings", {"offset": offset, "count": count})


def get_all_resource_file_names(offset=0, count=0):
    return get_from_jadx("all-resource-file-names", {"offset": offset, "count": count})


def get_resource_file(resource_name):
    return get_from_jadx("resource-file", {"resource_name": resource_name})
