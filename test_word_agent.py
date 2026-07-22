from pathlib import Path

from agents.word_agent import WordAgent


def main():
    test_output_folder = "outputs/test_word_documents"
    agent = WordAgent(output_folder=test_output_folder)
    result = agent.handle("帮我写一份项目阶段总结报告")

    if "Word Agent 已生成文档" not in result:
        raise AssertionError(f"没有生成文档：{result}")

    file_line = ""
    for line in result.splitlines():
        if line.startswith("文件位置："):
            file_line = line
            break

    if not file_line:
        raise AssertionError(f"结果中没有文件位置：{result}")

    document_path = Path(file_line.replace("文件位置：", "", 1))
    if not document_path.exists():
        raise AssertionError(f"文件不存在：{document_path}")

    document_content = document_path.read_text(encoding="utf-8")
    if "项目阶段总结报告" not in document_content:
        raise AssertionError("文档内容没有写入原始需求。")

    print(f"测试通过：Word Agent 已生成文件 {document_path}")


if __name__ == "__main__":
    main()
