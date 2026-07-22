from agents.file_improvement_agent import FileImprovementAgent
from agents.word_agent import WordAgent
from coordinator import ChiefCoordinator


def test_file_improvement_agent_builds_advice():
    word_agent = WordAgent(output_folder="outputs/test_file_improvement")
    word_result = word_agent.handle("帮我写一份需要优化的 Word 文档")
    document_path = extract_file_path(word_result)

    improvement_agent = FileImprovementAgent()
    result = improvement_agent.handle(f"请优化文件 {document_path}")

    required_texts = [
        "File Improvement Agent 已生成文件改进建议",
        "当前内容判断",
        "制作技巧建议",
        "分项改进建议",
        "素材与灵感来源",
        "文案修改",
        "版面设计",
        "图片建议",
    ]
    for text in required_texts:
        if text not in result:
            raise AssertionError(f"文件改进建议缺少内容：{text}")

    print("测试通过：File Improvement Agent 可以生成文件改进建议")


def test_coordinator_routes_file_improvement_task():
    word_agent = WordAgent(output_folder="outputs/test_file_improvement")
    word_result = word_agent.handle("帮我写一份用于协调器优化的 Word 文档")
    document_path = extract_file_path(word_result)

    coordinator = ChiefCoordinator()
    result = coordinator.handle_task(f"请优化文件 {document_path}")

    if "File Improvement Agent 已生成文件改进建议" not in result:
        raise AssertionError(f"Coordinator 没有分配给 File Improvement Agent：{result}")

    if "QA Agent 质量检查结果：跳过" not in result:
        raise AssertionError(f"文件改进任务应该跳过生成文件 QA：{result}")

    print("测试通过：Coordinator 可以分配文件改进任务")


def extract_file_path(task_result):
    for line in task_result.splitlines():
        if line.startswith("文件位置："):
            return line.replace("文件位置：", "", 1).strip()
    raise AssertionError(f"结果中没有文件位置：{task_result}")


def main():
    test_file_improvement_agent_builds_advice()
    test_coordinator_routes_file_improvement_task()


if __name__ == "__main__":
    main()
