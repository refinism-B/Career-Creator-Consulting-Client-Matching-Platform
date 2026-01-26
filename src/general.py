from pathlib import Path

def get_project_root() -> Path:
    """取得專案根目錄路徑"""
    return Path(__file__).resolve().parent.parent