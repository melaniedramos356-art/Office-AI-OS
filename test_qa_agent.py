from pathlib import Path

from agents.qa_agent import QAAgent
from coordinator import ChiefCoordinator


def test_qa_agent_directly():
    test_folder = Path("outputs/test_qa_files")
    test_folder.mkdir(parents=True, exist_ok=True)

    original_task = "帮我写一份测试报告"
    test_file = test_folder / "qa_test_document.md"
    test_file.write_text(f"# 测试文档\n\n{original_task}\n", encoding="utf-8")

    qa_agent = QAAgent()
    result = qa_agent.check_task_result(f"文件位置：{test_file}", original_task)

    if "QA Agent 质量检查结果：通过" not in result:
        raise AssertionError(f"QA Agent 直接检查失败：{result}")

    print("测试通过：QA Agent 可以直接检查文件")


def test_coordinator_with_qa_agent():
    coordinator = ChiefCoordinator()
    result = coordinator.handle_task("帮我写一份项目阶段总结报告")

    if "Word Agent 已生成文档" not in result:
        raise AssertionError(f"Word Agent 没有生成文档：{result}")

    if "QA Agent 质量检查结果：通过" not in result:
        raise AssertionError(f"Coordinator 没有自动触发 QA Agent：{result}")

    print("测试通过：Coordinator 已自动触发 QA Agent")


def main():
    test_qa_agent_directly()
    test_coordinator_with_qa_agent()


if __name__ == "__main__":
    main()
