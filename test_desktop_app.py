from desktop_app import build_desktop_command, command_needs_file, extract_first_output_path, load_panel_data


def main():
    buttons = load_panel_data().get("desktop_buttons", [])
    if len(buttons) < 6:
        raise AssertionError("桌面 App 没有加载到办公入口。")

    command = build_desktop_command("帮我做一份 {主题} PPT", "项目汇报")
    if command != "帮我做一份 项目汇报 PPT":
        raise AssertionError(f"桌面命令拼接错误：{command}")

    if not command_needs_file("请生成改进版 {文件路径}"):
        raise AssertionError("没有识别出需要文件路径的命令。")

    output_path = extract_first_output_path("已生成 ChatGPT App 创作任务单。\n任务单位置：outputs\\creation_briefs\\demo.md")
    if output_path != "outputs\\creation_briefs\\demo.md":
        raise AssertionError(f"桌面 App 未识别任务单路径：{output_path}")

    print("测试通过：桌面 App 可以识别创作任务单")


if __name__ == "__main__":
    main()
