import os
import sys


def get_project_root():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


PROJECT_ROOT = get_project_root()
TMP_DIR = os.path.join(PROJECT_ROOT, 'tmp')
RESULT_DIR = os.path.join(PROJECT_ROOT, 'result')
SCRIPTS_DIR = os.path.join(PROJECT_ROOT, 'scripts')


def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    return path


def tmp_path(filename):
    ensure_dir(TMP_DIR)
    return os.path.join(TMP_DIR, filename)


def result_path(filename):
    ensure_dir(RESULT_DIR)
    return os.path.join(RESULT_DIR, filename)


def scripts_path(filename):
    return os.path.join(SCRIPTS_DIR, filename)


def save_tmp(filename, content, mode='w', encoding='utf-8'):
    filepath = tmp_path(filename)
    with open(filepath, mode, encoding=encoding) as f:
        f.write(content)
    return filepath


def save_result(filename, content, mode='w', encoding='utf-8'):
    filepath = result_path(filename)
    with open(filepath, mode, encoding=encoding) as f:
        f.write(content)
    return filepath
