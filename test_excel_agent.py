from pathlib import Path
from zipfile import ZipFile

from agents.excel_agent import ExcelAgent
from agents.qa_agent import QAAgent


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

    if table_path.suffix.lower() != ".xlsx":
        raise AssertionError(f"Excel Agent 应该生成 .xlsx 文件，实际是：{table_path}")

    with ZipFile(table_path, "r") as xlsx_file:
        xlsx_file.read("xl/workbook.xml")
        xlsx_file.read("xl/worksheets/sheet1.xml")

    qa_agent = QAAgent()
    table_content = qa_agent.read_file_content(table_path)
    if "客户数据" not in table_content:
        raise AssertionError("表格内容没有写入原始需求。")

    if "素材库生成建议" not in table_content:
        raise AssertionError("Excel 表格没有写入素材库生成建议。")

    if "DeepSeek 字段建议" not in table_content:
        raise AssertionError("Excel 表格没有写入 DeepSeek 字段建议。")

    if "表格使用说明" not in table_content:
        raise AssertionError("Excel 表格没有写入表格使用说明。")

    if "数据填写规则" not in table_content:
        raise AssertionError("Excel 表格没有写入数据填写规则。")

    if "推荐分析图表" not in table_content:
        raise AssertionError("Excel 表格没有写入推荐分析图表。")

    if "质量检查清单" not in table_content:
        raise AssertionError("Excel 表格没有写入质量检查清单。")

    if "数据分析网站灵感库" not in table_content:
        raise AssertionError("Excel 表格没有写入数据分析网站灵感库。")

    if "Tableau Public" not in table_content or "Power BI Data Stories Gallery" not in table_content:
        raise AssertionError("Excel 表格没有写入核心数据分析灵感网站。")

    if "Flourish Examples" not in table_content:
        raise AssertionError("Excel 表格没有写入图表灵感网站。")

    print(f"测试通过：Excel Agent 已生成文件 {table_path}")


if __name__ == "__main__":
    main()
