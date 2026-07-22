import os
from pathlib import Path
from zipfile import ZipFile

from agents.word_agent import WordAgent
from agents.qa_agent import QAAgent

os.environ["OFFICE_AI_USE_REAL_MODEL"] = "0"


def main():
    test_word_agent_builds_report()
    test_word_agent_builds_student_summer_safety_script()
    test_word_agent_builds_low_altitude_capital_report()
    test_word_agent_builds_class_monitor_speech()


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

    assert_no_prompt_like_content(document_content)

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

    assert_no_prompt_like_content(document_content)

    print(f"测试通过：Word Agent 已生成大学生暑假安全班会文案 {document_path}")


def test_word_agent_builds_low_altitude_capital_report():
    test_output_folder = "outputs/test_word_documents"
    agent = WordAgent(output_folder=test_output_folder)
    result = agent.handle("生成关于资本赋能低空经济产业发展研究的 Word 文档")
    document_path = extract_file_path(result)

    qa_agent = QAAgent()
    document_content = qa_agent.read_file_content(document_path)
    required_texts = [
        "《资本赋能低空经济产业发展研究》",
        "含义解析",
        "江西低空经济发展基础",
        "资本赋能低空经济的主要痛点",
        "资本赋能路径建议",
        "结论",
    ]

    for text in required_texts:
        if text not in document_content:
            raise AssertionError(f"低空经济研究报告缺少内容：{text}")

    assert_no_prompt_like_content(document_content)

    print(f"测试通过：Word Agent 已生成低空经济研究报告 {document_path}")


def test_word_agent_builds_class_monitor_speech():
    test_output_folder = "outputs/test_word_documents"
    agent = WordAgent(output_folder=test_output_folder)
    result = agent.handle("帮我写一份大学生竞选班长的发言稿")
    document_path = extract_file_path(result)

    qa_agent = QAAgent()
    document_content = qa_agent.read_file_content(document_path)
    required_texts = [
        "大学生竞选班长发言稿",
        "开场问候",
        "竞选理由",
        "工作设想",
        "服务承诺",
        "结尾表态",
    ]

    for text in required_texts:
        if text not in document_content:
            raise AssertionError(f"大学生竞选班长发言稿缺少内容：{text}")

    assert_no_prompt_like_content(document_content)

    print(f"测试通过：Word Agent 已生成大学生竞选班长发言稿 {document_path}")


def extract_file_path(task_result):
    for line in task_result.splitlines():
        if line.startswith("文件位置："):
            return Path(line.replace("文件位置：", "", 1).strip())
    raise AssertionError(f"结果中没有文件位置：{task_result}")


def assert_no_prompt_like_content(document_content):
    forbidden_texts = [
        "AI 结构建议",
        "通用制作技巧",
        "灵感素材查找建议",
        "素材库生成建议",
        "搜索词",
        "请在这里填写",
        "请替换",
        "示例",
        "草稿",
        "继续补充",
        "预留",
        "Dribbble",
        "Behance",
        "图片生成提示词",
    ]

    for text in forbidden_texts:
        if text in document_content:
            raise AssertionError(f"Word 成品文件不应该包含提示词类内容：{text}")


if __name__ == "__main__":
    main()
