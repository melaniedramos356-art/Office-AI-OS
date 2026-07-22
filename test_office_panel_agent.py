from pathlib import Path

from agents.office_panel_agent import OfficePanelAgent
from coordinator import ChiefCoordinator


def test_office_panel_agent_directly():
    test_output_folder = "outputs/test_office_panels"
    agent = OfficePanelAgent(output_folder=test_output_folder)
    result = agent.handle("请完善办公板块，准备做桌面 App 交互页面")

    if "Office Panel Agent 已生成办公板块说明" not in result:
        raise AssertionError(f"没有生成办公板块说明：{result}")

    panel_path = extract_file_path(result)
    if not panel_path.exists():
        raise AssertionError(f"文件不存在：{panel_path}")

    panel_content = panel_path.read_text(encoding="utf-8")
    required_texts = [
        "Word 文档生成",
        "PPT 演示生成",
        "Excel 表格生成",
        "已有文件改进",
        "素材灵感计划",
        "桌面 App 按钮建议",
    ]
    for text in required_texts:
        if text not in panel_content:
            raise AssertionError(f"办公板块说明缺少内容：{text}")

    print(f"测试通过：Office Panel Agent 已生成文件 {panel_path}")


def test_coordinator_routes_office_panel_task():
    coordinator = ChiefCoordinator()
    result = coordinator.handle_task("请完善办公板块，准备做桌面 App 交互页面")

    if "Office Panel Agent 已生成办公板块说明" not in result:
        raise AssertionError(f"Coordinator 没有分配给 Office Panel Agent：{result}")

    if "QA Agent 质量检查结果：通过" not in result:
        raise AssertionError(f"Office Panel Agent 结果没有通过 QA：{result}")

    print("测试通过：Coordinator 可以分配办公板块任务")


def extract_file_path(task_result):
    for line in task_result.splitlines():
        if line.startswith("文件位置："):
            return Path(line.replace("文件位置：", "", 1).strip())
    raise AssertionError(f"结果中没有文件位置：{task_result}")


def main():
    test_office_panel_agent_directly()
    test_coordinator_routes_office_panel_task()


if __name__ == "__main__":
    main()
