from pathlib import Path
from zipfile import ZipFile

from agents.word_agent import WordAgent
from agents.qa_agent import QAAgent


def main():
    test_word_agent_builds_report()
    test_word_agent_builds_student_summer_safety_script()


def test_word_agent_builds_report():
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

    if document_path.suffix.lower() != ".docx":
        raise AssertionError(f"Word Agent 应该生成 .docx 文件，实际是：{document_path}")

    with ZipFile(document_path, "r") as docx_file:
        docx_file.read("word/document.xml")

    qa_agent = QAAgent()
    document_content = qa_agent.read_file_content(document_path)
    if "项目阶段总结报告" not in document_content:
        raise AssertionError("文档内容没有写入原始需求。")

    if "文档摘要" not in document_content:
        raise AssertionError("Word 文档没有写入文档摘要。")

    if "AI 结构建议" not in document_content:
        raise AssertionError("Word 文档没有写入 AI 结构建议。")

    if "通用制作技巧" not in document_content:
        raise AssertionError("Word 文档没有写入通用制作技巧。")

    if "版面设计" not in document_content or "文案生成" not in document_content:
        raise AssertionError("Word 文档没有写入版面设计和文案生成技巧。")

    if "图片查找" not in document_content or "图片生成" not in document_content:
        raise AssertionError("Word 文档没有写入图片相关制作技巧。")

    if "灵感素材查找建议" not in document_content:
        raise AssertionError("Word 文档没有写入灵感素材查找建议。")

    if "Dribbble" not in document_content or "Behance" not in document_content:
        raise AssertionError("Word 文档没有写入核心灵感网站。")

    if "素材库生成建议" not in document_content:
        raise AssertionError("Word 文档没有写入素材库生成建议。")

    print(f"测试通过：Word Agent 已生成文件 {document_path}")


def test_word_agent_builds_student_summer_safety_script():
    test_output_folder = "outputs/test_word_documents"
    agent = WordAgent(output_folder=test_output_folder)
    result = agent.handle("帮我写一份大学生暑假安全宣传教育班会的文案")
    document_path = extract_file_path(result)

    qa_agent = QAAgent()
    document_content = qa_agent.read_file_content(document_path)
    required_texts = [
        "大学生暑假安全宣传教育主题班会文案",
        "班会主题",
        "防溺水",
        "网络诈骗",
        "兼职实习安全",
        "结束语",
    ]

    for text in required_texts:
        if text not in document_content:
            raise AssertionError(f"大学生暑假安全班会文案缺少内容：{text}")

    if "请在这里填写" in document_content:
        raise AssertionError("大学生暑假安全班会文案不应该再出现模板占位文字。")

    print(f"测试通过：Word Agent 已生成大学生暑假安全班会文案 {document_path}")


def extract_file_path(task_result):
    for line in task_result.splitlines():
        if line.startswith("文件位置："):
            return Path(line.replace("文件位置：", "", 1).strip())
    raise AssertionError(f"结果中没有文件位置：{task_result}")


if __name__ == "__main__":
    main()
