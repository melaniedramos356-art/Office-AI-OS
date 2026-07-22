from pathlib import Path

from agents.word_agent import WordAgent


def main():
    result = WordAgent().handle("生成一份大学生竞选班长的发言稿")
    brief_path = extract_brief_path(result)
    content = brief_path.read_text(encoding="utf-8")

    for text in ["Word 文档 创作任务单", "大学生竞选班长", "Word 专项要求", "最终制作指令"]:
        if text not in content:
            raise AssertionError(f"Word 任务单缺少内容：{text}")
    print(f"测试通过：已生成 Word 创作任务单 {brief_path}")


def extract_brief_path(result):
    for line in result.splitlines():
        if line.startswith("任务单位置："):
            return Path(line.replace("任务单位置：", "", 1).strip())
    raise AssertionError(f"未找到任务单位置：{result}")


if __name__ == "__main__":
    main()
