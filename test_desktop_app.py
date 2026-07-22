from desktop_app import build_desktop_command, command_needs_file, load_panel_data


def test_load_panel_data():
    panel_data = load_panel_data()
    buttons = panel_data.get("desktop_buttons", [])

    if len(buttons) < 6:
        raise AssertionError("桌面 App 没有加载到足够的办公按钮。")

    labels = [button.get("label", "") for button in buttons]
    required_labels = ["新建 Word", "新建 PPT", "新建 Excel", "改进文件", "找素材"]
    for label in required_labels:
        if label not in labels:
            raise AssertionError(f"桌面 App 缺少按钮：{label}")

    print("测试通过：桌面 App 可以加载办公按钮数据")


def test_build_desktop_command():
    word_command = build_desktop_command("帮我写一份{主题} Word 文档", "项目总结")
    if word_command != "帮我写一份项目总结 Word 文档":
        raise AssertionError(f"Word 命令拼接错误：{word_command}")

    empty_word_command = build_desktop_command("帮我写一份{主题} Word 文档", "")
    if empty_word_command:
        raise AssertionError(f"空主题不应该生成命令：{empty_word_command}")

    file_command = build_desktop_command("请生成改进版 {文件路径}", "", "C:\\test\\demo.docx")
    if file_command != "请生成改进版 C:\\test\\demo.docx":
        raise AssertionError(f"文件改进命令拼接错误：{file_command}")

    if not command_needs_file("请生成改进版 {文件路径}"):
        raise AssertionError("没有识别出需要文件路径的命令。")

    print("测试通过：桌面 App 可以拼接执行命令")


def main():
    test_load_panel_data()
    test_build_desktop_command()


if __name__ == "__main__":
    main()
