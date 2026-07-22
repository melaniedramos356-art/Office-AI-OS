from pathlib import Path

from agents.file_improvement_agent import FileImprovementAgent


def main():
    source_path = Path("outputs/test_sources/improve_source.pptx")
    source_path.parent.mkdir(parents=True, exist_ok=True)
    source_path.write_bytes(b"test")

    result = FileImprovementAgent().handle(f"请优化文件 {source_path}")
    brief_path = extract_brief_path(result)
    content = brief_path.read_text(encoding="utf-8")

    for text in ["PPT 演示文稿 创作任务单", "请同时上传并读取", "重点提升内容、语言、版式", "PPT 专项要求"]:
        if text not in content:
            raise AssertionError(f"文件改进任务单缺少内容：{text}")
    print(f"测试通过：已生成文件改进任务单 {brief_path}")


def extract_brief_path(result):
    for line in result.splitlines():
        if line.startswith("任务单位置："):
            return Path(line.replace("任务单位置：", "", 1).strip())
    raise AssertionError(f"未找到任务单位置：{result}")


if __name__ == "__main__":
    main()
