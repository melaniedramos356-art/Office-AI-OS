from pathlib import Path

from agents.excel_agent import ExcelAgent


def main():
    test_output_folder = "outputs/test_excel_files"
    agent = ExcelAgent(output_folder=test_output_folder)
    result = agent.handle("帮我整理一份客户数据 Excel 表格")

    if "Excel Agent 已生成表格" not in result:
        raise AssertionError(f"没有生成表格：{result}")

    file_line = ""
    for line in result.splitlines():
        if line.startswith("文件位置："):
            file_line = line
            break

    if not file_line:
        raise AssertionError(f"结果中没有文件位置：{result}")

    table_path = Path(file_line.replace("文件位置：", "", 1))
    if not table_path.exists():
        raise AssertionError(f"文件不存在：{table_path}")

    table_content = table_path.read_text(encoding="utf-8-sig")
    if "客户数据" not in table_content:
        raise AssertionError("表格内容没有写入原始需求。")

    print(f"测试通过：Excel Agent 已生成文件 {table_path}")


if __name__ == "__main__":
    main()
