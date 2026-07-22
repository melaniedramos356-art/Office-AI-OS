from agents.file_reader_agent import FileReaderAgent
from agents.word_agent import WordAgent
from coordinator import ChiefCoordinator


def test_file_reader_agent_reads_docx():
    word_agent = WordAgent(output_folder="outputs/test_file_reader")
    word_result = word_agent.handle("帮我写一份测试读取文件的 Word 文档")
    document_path = extract_file_path(word_result)

    reader_agent = FileReaderAgent()
    result = reader_agent.handle(f"读取文件 {document_path}")

    if "File Reader Agent 已读取文件" not in result:
        raise AssertionError(f"File Reader Agent 没有读取文件：{result}")

    if "内容预览" not in result:
        raise AssertionError("File Reader Agent 没有输出内容预览。")

    if "Word Agent" not in result:
        raise AssertionError("File Reader Agent 没有给出 Word 下一步建议。")

    print("测试通过：File Reader Agent 可以读取 docx 文件")


def test_coordinator_routes_file_reader_task():
    word_agent = WordAgent(output_folder="outputs/test_file_reader")
    word_result = word_agent.handle("帮我写一份用于协调器读取的 Word 文档")
    document_path = extract_file_path(word_result)

    coordinator = ChiefCoordinator()
    result = coordinator.handle_task(f"请分析文件 {document_path}")

    if "File Reader Agent 已读取文件" not in result:
        raise AssertionError(f"Coordinator 没有分配给 File Reader Agent：{result}")

    if "QA Agent 质量检查结果：跳过" not in result:
        raise AssertionError(f"File Reader Agent 文件读取任务应该跳过生成文件 QA：{result}")

    print("测试通过：Coordinator 可以分配文件读取任务")


def extract_file_path(task_result):
    for line in task_result.splitlines():
        if line.startswith("文件位置："):
            return line.replace("文件位置：", "", 1).strip()
    raise AssertionError(f"结果中没有文件位置：{task_result}")


def main():
    test_file_reader_agent_reads_docx()
    test_coordinator_routes_file_reader_task()


if __name__ == "__main__":
    main()
