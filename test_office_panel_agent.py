from agents.office_panel_agent import OfficePanelAgent


def main():
    agent = OfficePanelAgent(output_folder="outputs/test_office_panels")
    data = agent.build_panel_data("桌面程序交互页面")
    buttons = data.get("desktop_buttons", [])
    labels = [button.get("label") for button in buttons]

    for label in ["新建 Word", "新建 PPT", "新建 Excel", "改进文件", "参考仿写"]:
        if label not in labels:
            raise AssertionError(f"办公面板缺少入口：{label}")

    result = agent.handle("桌面程序交互页面")
    if "办公面板说明" not in result:
        raise AssertionError(f"办公面板说明生成失败：{result}")
    print("测试通过：办公面板使用创作任务单入口")


if __name__ == "__main__":
    main()
