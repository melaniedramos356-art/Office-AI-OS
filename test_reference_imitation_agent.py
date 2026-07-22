from pathlib import Path

from agents.reference_imitation_agent import ReferenceImitationAgent
from agents.qa_agent import QAAgent
from coordinator import ChiefCoordinator


def main():
    test_reference_imitation_agent_builds_word()
    test_coordinator_routes_reference_imitation()


def test_reference_imitation_agent_builds_word():
    source_folder = Path("outputs/test_reference_sources")
    source_folder.mkdir(parents=True, exist_ok=True)
    source_path = source_folder / "reference.docx"

    agent = ReferenceImitationAgent()
    agent.word_agent.output_folder = source_folder
    agent.word_agent.write_docx(
        source_path,
        [
            ("title", "参考文档"),
            ("heading", "一、背景"),
            ("text", "这是参考文件背景。"),
            ("heading", "二、目标"),
            ("text", "这是参考文件目标。"),
        ],
    )

    result = agent.handle(f"请参考 {source_path} 仿写一份关于大学生竞选班长的 Word 文档")
    if "Reference Imitation Agent 已生成参考仿写 Word 成品文件" not in result:
        raise AssertionError(f"没有生成参考仿写 Word：{result}")

    output_path = extract_file_path(result)
    if not output_path.exists():
        raise AssertionError(f"参考仿写文件不存在：{output_path}")

    content = QAAgent().read_file_content(output_path)
    required_texts = ["大学生竞选班长", "文档摘要", "背景", "目标"]
    for text in required_texts:
        if text not in content:
            raise AssertionError(f"参考仿写 Word 缺少内容：{text}")

    forbidden_texts = ["提示词", "请替换", "待采集", "需补充"]
    for text in forbidden_texts:
        if text in content:
            raise AssertionError(f"参考仿写 Word 不应包含占位内容：{text}")

    print(f"测试通过：Reference Imitation Agent 已生成 Word 仿写文件 {output_path}")


def test_coordinator_routes_reference_imitation():
    coordinator = ChiefCoordinator()
    agent = coordinator.choose_agent("请仿写 C:\\test\\demo.docx 生成新文档")
    if agent.__class__.__name__ != "ReferenceImitationAgent":
        raise AssertionError(f"Coordinator 没有分配给 ReferenceImitationAgent：{agent.__class__.__name__}")

    print("测试通过：Coordinator 可以分配参考仿写任务")


def extract_file_path(task_result):
    for line in task_result.splitlines():
        if line.startswith("文件位置："):
            return Path(line.replace("文件位置：", "", 1).strip())
    raise AssertionError(f"结果中没有文件位置：{task_result}")


if __name__ == "__main__":
    main()
