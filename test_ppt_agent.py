import os
from pathlib import Path
from zipfile import ZipFile

from agents.ppt_agent import PPTAgent
from agents.qa_agent import QAAgent

os.environ["OFFICE_AI_USE_REAL_MODEL"] = "0"


def main():
    test_output_folder = "outputs/test_ppt_outlines"
    agent = PPTAgent(output_folder=test_output_folder)
    result = agent.handle("帮我做一份项目阶段汇报 PPT")

    if "PPT Agent 已生成 PPT 文件" not in result:
        raise AssertionError(f"没有生成 PPT 文件：{result}")

    file_line = ""
    for line in result.splitlines():
        if line.startswith("文件位置："):
            file_line = line
            break

    if not file_line:
        raise AssertionError(f"结果中没有文件位置：{result}")

    presentation_path = Path(file_line.replace("文件位置：", "", 1))
    if not presentation_path.exists():
        raise AssertionError(f"文件不存在：{presentation_path}")

    if presentation_path.suffix.lower() != ".pptx":
        raise AssertionError(f"PPT Agent 应该生成 .pptx 文件，实际是：{presentation_path}")

    with ZipFile(presentation_path, "r") as pptx_file:
        pptx_file.read("ppt/presentation.xml")
        pptx_file.read("ppt/slides/slide1.xml")

    qa_agent = QAAgent()
    presentation_content = qa_agent.read_file_content(presentation_path)
    if "项目阶段汇报" not in presentation_content:
        raise AssertionError("PPT 文件没有写入原始需求。")

    if "目录" not in presentation_content:
        raise AssertionError("PPT 文件没有写入目录页。")

    if "项目已进入可控推进阶段" not in presentation_content:
        raise AssertionError("PPT 文件没有使用结论式页面标题。")

    forbidden_texts = [
        "AI 结构建议",
        "通用制作技巧",
        "灵感素材查找建议",
        "素材库生成建议",
        "搜索词",
        "提示词",
        "请在这里填写",
        "请替换",
        "示例",
        "草稿",
        "预留",
        "Dribbble",
        "Behance",
    ]
    for text in forbidden_texts:
        if text in presentation_content:
            raise AssertionError(f"PPT 成品文件不应该包含提示词类内容：{text}")

    print(f"测试通过：PPT Agent 已生成文件 {presentation_path}")


if __name__ == "__main__":
    main()
