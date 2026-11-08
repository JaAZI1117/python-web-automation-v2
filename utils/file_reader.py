import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

def load_json(file_name):
    """读取 data/ 下的 JSON，路径不受运行目录影响"""
    with open(DATA_DIR / file_name, "r", encoding="utf-8") as f:
        return json.load(f)

def load_cases(file_name):
    """兼容裸列表和 {'cases': [...]} 两种写法"""
    data = load_json(file_name)
    return data["cases"] if isinstance(data, dict) else data
