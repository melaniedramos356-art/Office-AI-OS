from pathlib import Path

from agents.excel_agent import ExcelAgent


def main():
    result = ExcelAgent().handle("制作一份销售数据分析 Excel，包含趋势和异常提醒")
    brief_path = extract_brief_path(result)
    content = brief_path.read_text(encoding="utf-8")

    for text in ["Excel 工作簿 创作任务单", "销售数据分析", "Excel 专项要求", "关键公式"]:
        if text not in content:
            raise AssertionError(f"Excel 任务单缺少内容：{text}")
    print(f"测试通过：已生成 Excel 创作任务单 {brief_path}")


def extract_brief_path(result):
    for line in result.splitlines():
        if line.startswith("任务单位置："):
            return Path(line.replace("任务单位置：", "", 1).strip())
    raise AssertionError(f"未找到任务单位置：{result}")


if __name__ == "__main__":
    main()
