from pathlib import Path

from agents.reference_imitation_agent import ReferenceImitationAgent


def main():
    source_path = Path("outputs/test_sources/reference_source.docx")
    source_path.parent.mkdir(parents=True, exist_ok=True)
    source_path.write_bytes(b"test")

    result = ReferenceImitationAgent().handle(f"请参考 {source_path} 仿写一份大学生竞选班长的 Word 文档")
    brief_path = extract_brief_path(result)
    content = brief_path.read_text(encoding="utf-8")

    for text in ["Word 文档 创作任务单", "以新主题重新创作", "大学生竞选班长", "Word 专项要求"]:
        if text not in content:
            raise AssertionError(f"参考仿写任务单缺少内容：{text}")
    print(f"测试通过：已生成参考仿写任务单 {brief_path}")


def extract_brief_path(result):
    for line in result.splitlines():
        if line.startswith("任务单位置："):
            return Path(line.replace("任务单位置：", "", 1).strip())
    raise AssertionError(f"未找到任务单位置：{result}")


if __name__ == "__main__":
    main()
