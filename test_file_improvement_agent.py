from pathlib import Path

from agents.file_improvement_agent import FileImprovementAgent
from agents.excel_agent import ExcelAgent
from agents.ppt_agent import PPTAgent
from agents.qa_agent import QAAgent
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
        "站酷",
        "花瓣",
    ]
    for text in required_texts:
        if text not in result:
            raise AssertionError(f"文件改进建议缺少内容：{text}")

    print("测试通过：File Improvement Agent 可以生成文件改进建议")


def test_file_improvement_agent_creates_word_file():
    word_agent = WordAgent(output_folder="outputs/test_file_improvement")
    word_result = word_agent.handle("帮我写一份需要生成改进版的 Word 文档")
    original_document_path = extract_file_path(word_result)

    improvement_agent = FileImprovementAgent()
    result = improvement_agent.handle(f"请生成改进版 {original_document_path}")

    if "File Improvement Agent 已生成 Word 改进版文件" not in result:
        raise AssertionError(f"File Improvement Agent 没有生成 Word 改进版：{result}")

    improved_document_path = extract_file_path(result)
    if improved_document_path == original_document_path:
        raise AssertionError("改进版文件不应该覆盖原文件。")

    qa_agent = QAAgent()
    improved_content = qa_agent.read_file_content(Path(improved_document_path))
    required_texts = ["Word 改进版文档", "结构优化建议", "文案润色方向", "版面设计方向", "图片素材建议"]
    for text in required_texts:
        if text not in improved_content:
            raise AssertionError(f"Word 改进版缺少内容：{text}")

    print("测试通过：File Improvement Agent 可以生成 Word 改进版文件")


def test_file_improvement_agent_creates_ppt_file():
    ppt_agent = PPTAgent(output_folder="outputs/test_file_improvement")
    ppt_result = ppt_agent.handle("帮我做一份需要生成改进版的 PPT")
    original_ppt_path = extract_file_path(ppt_result)

    improvement_agent = FileImprovementAgent()
    result = improvement_agent.handle(f"请生成改进版 {original_ppt_path}")

    if "File Improvement Agent 已生成 PPT 改进版文件" not in result:
        raise AssertionError(f"File Improvement Agent 没有生成 PPT 改进版：{result}")

    improved_ppt_path = extract_file_path(result)
    qa_agent = QAAgent()
    improved_content = qa_agent.read_file_content(Path(improved_ppt_path))
    required_texts = ["PPT 改进版", "页面结构优化", "结论式标题建议", "版面设计建议", "图片素材建议"]
    for text in required_texts:
        if text not in improved_content:
            raise AssertionError(f"PPT 改进版缺少内容：{text}")

    print("测试通过：File Improvement Agent 可以生成 PPT 改进版文件")


def test_file_improvement_agent_creates_excel_file():
    excel_agent = ExcelAgent(output_folder="outputs/test_file_improvement")
    excel_result = excel_agent.handle("帮我整理一份需要生成改进版的 Excel 表格")
    original_excel_path = extract_file_path(excel_result)

    improvement_agent = FileImprovementAgent()
    result = improvement_agent.handle(f"请生成改进版 {original_excel_path}")

    if "File Improvement Agent 已生成 Excel 改进版文件" not in result:
        raise AssertionError(f"File Improvement Agent 没有生成 Excel 改进版：{result}")

    improved_excel_path = extract_file_path(result)
    qa_agent = QAAgent()
    improved_content = qa_agent.read_file_content(Path(improved_excel_path))
    required_texts = ["Excel 改进版", "字段检查", "数据填写规则", "推荐分析图表", "质量检查清单"]
    for text in required_texts:
        if text not in improved_content:
            raise AssertionError(f"Excel 改进版缺少内容：{text}")

    print("测试通过：File Improvement Agent 可以生成 Excel 改进版文件")


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
    test_file_improvement_agent_creates_word_file()
    test_file_improvement_agent_creates_ppt_file()
    test_file_improvement_agent_creates_excel_file()
    test_coordinator_routes_file_improvement_task()


if __name__ == "__main__":
    main()
