import csv
from datetime import datetime
from pathlib import Path


class ExcelAgent:
    def __init__(self, output_folder="outputs/excel_files"):
        self.output_folder = Path(output_folder)

    def handle(self, user_task):
        if not isinstance(user_task, str) or not user_task.strip():
            return "Excel Agent 没有收到有效任务。"

        cleaned_task = user_task.strip()

        try:
            table_path = self.create_table(cleaned_task)
        except OSError as error:
            return f"Excel Agent 创建表格失败：{error}"

        return (
            "Excel Agent 已生成表格。\n"
            f"任务内容：{cleaned_task}\n"
            f"文件位置：{table_path}"
        )

    def create_table(self, user_task):
        self.output_folder.mkdir(parents=True, exist_ok=True)

        file_name = self.build_file_name()
        table_path = self.output_folder / file_name
        rows = self.build_rows(user_task)

        with table_path.open("w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            writer.writerows(rows)

        return table_path

    def build_file_name(self):
        time_text = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        return f"excel_table_{time_text}.csv"

    def build_rows(self, user_task):
        table_type = self.detect_table_type(user_task)

        if table_type == "数据统计表":
            return [
                ["表格类型", "数据统计表"],
                ["原始需求", user_task],
                [],
                ["项目", "数值", "备注"],
                ["示例项目A", "0", "请替换为真实数据"],
                ["示例项目B", "0", "请替换为真实数据"],
                ["合计", "0", "请填写计算结果"],
            ]

        if table_type == "客户信息表":
            return [
                ["表格类型", "客户信息表"],
                ["原始需求", user_task],
                [],
                ["客户名称", "联系人", "电话", "跟进状态", "备注"],
                ["示例客户A", "", "", "待跟进", "请替换为真实客户"],
                ["示例客户B", "", "", "待跟进", "请替换为真实客户"],
            ]

        if table_type == "销售报表":
            return [
                ["表格类型", "销售报表"],
                ["原始需求", user_task],
                [],
                ["日期", "产品", "销售额", "成本", "利润", "备注"],
                ["2026-07-22", "示例产品", "0", "0", "0", "请替换为真实数据"],
            ]

        return [
            ["表格类型", "通用表格"],
            ["原始需求", user_task],
            [],
            ["序号", "事项", "负责人", "状态", "备注"],
            ["1", "示例事项", "", "未开始", "请替换为真实内容"],
        ]

    def detect_table_type(self, user_task):
        if "客户" in user_task:
            return "客户信息表"

        if "销售" in user_task or "营收" in user_task or "收入" in user_task:
            return "销售报表"

        if "统计" in user_task or "数据" in user_task or "计算" in user_task:
            return "数据统计表"

        return "通用表格"
