from pathlib import Path


def test_shortcut_scripts_exist():
    batch_path = Path("create_desktop_shortcut.bat")
    powershell_path = Path("scripts/create_desktop_shortcut.ps1")

    if not batch_path.exists():
        raise AssertionError("缺少桌面图标创建入口：create_desktop_shortcut.bat")

    if not powershell_path.exists():
        raise AssertionError("缺少桌面图标创建脚本：scripts/create_desktop_shortcut.ps1")

    print("测试通过：桌面图标创建脚本存在")


def test_shortcut_script_content():
    powershell_text = Path("scripts/create_desktop_shortcut.ps1").read_text(encoding="utf-8")
    required_texts = [
        "Office-AI-OS.lnk",
        "start_desktop_app.bat",
        "WScript.Shell",
        "IconLocation",
    ]

    for text in required_texts:
        if text not in powershell_text:
            raise AssertionError(f"桌面图标创建脚本缺少内容：{text}")

    print("测试通过：桌面图标创建脚本内容完整")


def main():
    test_shortcut_scripts_exist()
    test_shortcut_script_content()


if __name__ == "__main__":
    main()
