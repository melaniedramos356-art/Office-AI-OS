from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape
from zipfile import ZIP_DEFLATED, ZipFile

from agents.ai_output_utils import extract_json_data, has_forbidden_output_text, is_usable_model_generation
from models.model_router import ModelRouter


class ExcelAgent:
    def __init__(self, output_folder="outputs/excel_files", model_router=None):
        self.output_folder = Path(output_folder)
        self.model_router = model_router or ModelRouter()

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

        self.write_xlsx(table_path, rows)
        return table_path

    def build_file_name(self):
        time_text = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        return f"excel_table_{time_text}.xlsx"

    def build_rows(self, user_task):
        table_type = self.detect_table_type(user_task)
        table_topic = self.extract_table_topic(user_task)
        ai_rows = self.build_ai_rows(user_task, table_type, table_topic)
        if ai_rows:
            return self.add_support_rows(ai_rows)

        if table_type == "数据统计表":
            rows = [
                ["表格类型", "数据统计表"],
                ["表格主题", table_topic],
                [],
                ["项目", "数值", "备注"],
                ["核心指标", "128", "本期重点统计值"],
                ["阶段成果", "36", "已完成事项数量"],
                ["风险事项", "5", "需要持续跟踪"],
                ["合计", "169", "核心指标、阶段成果和风险事项汇总"],
            ]
            return self.add_support_rows(rows)

        if table_type == "客户信息表":
            rows = [
                ["表格类型", "客户信息表"],
                ["表格主题", table_topic],
                [],
                ["客户名称", "联系人", "电话", "跟进状态", "备注"],
                ["星辰科技有限公司", "张经理", "13800000001", "跟进中", "已完成需求沟通"],
                ["远航教育集团", "李老师", "13800000002", "待跟进", "本周安排首次沟通"],
                ["华信商贸有限公司", "王主管", "13800000003", "已成交", "已确认合作方案"],
            ]
            return self.add_support_rows(rows)

        if table_type == "销售报表":
            rows = [
                ["表格类型", "销售报表"],
                ["表格主题", table_topic],
                [],
                ["日期", "产品", "销售额", "成本", "利润", "备注"],
                ["2026-07-20", "核心产品A", "120000", "72000", "48000", "利润率40%"],
                ["2026-07-21", "核心产品B", "86000", "55900", "30100", "利润率35%"],
                ["2026-07-22", "增值服务包", "46000", "18400", "27600", "利润率60%"],
            ]
            return self.add_support_rows(rows)

        rows = [
            ["表格类型", "通用表格"],
            ["表格主题", table_topic],
            [],
            ["序号", "事项", "负责人", "状态", "备注"],
            ["1", "资料整理", "负责人A", "进行中", "已完成初步汇总"],
            ["2", "内容核对", "负责人B", "未开始", "计划今日处理"],
            ["3", "结果交付", "负责人C", "未开始", "完成后统一归档"],
        ]
        return self.add_support_rows(rows)

    def build_ai_rows(self, user_task, table_type, table_topic):
        headers = self.build_headers(table_type)
        prompt = (
            f"需求：{user_task}\n"
            f"表格类型：{table_type}\n"
            f"表格主题：{table_topic}\n"
            f"表头：{headers}\n"
            "返回JSON：{\"rows\":[[\"字段1\",\"字段2\"],[\"数据1\",\"数据2\"]]}\n"
            "要求：第一行必须是表格类型，第二行必须是表格主题，第三行空数组，第四行必须是给定表头；后面生成3到6行可直接查看的业务数据；不要提示词、搜索词、占位、示例、草稿、待采集、按实际、需补充。"
        )
        generation = self.model_router.generate("excel", prompt)
        if not is_usable_model_generation(generation):
            return []

        data = extract_json_data(generation.get("result", ""))
        if not isinstance(data, dict) or has_forbidden_output_text(data):
            return []

        rows = data.get("rows", [])
        if not self.is_valid_ai_rows(rows, table_type, table_topic, headers):
            return []

        return rows

    def build_headers(self, table_type):
        if table_type == "数据统计表":
            return ["项目", "数值", "备注"]
        if table_type == "客户信息表":
            return ["客户名称", "联系人", "电话", "跟进状态", "备注"]
        if table_type == "销售报表":
            return ["日期", "产品", "销售额", "成本", "利润", "备注"]
        return ["序号", "事项", "负责人", "状态", "备注"]

    def is_valid_ai_rows(self, rows, table_type, table_topic, headers):
        if not isinstance(rows, list) or len(rows) < 5:
            return False

        if rows[0] != ["表格类型", table_type]:
            return False

        if rows[1] != ["表格主题", table_topic]:
            return False

        if rows[2] != []:
            return False

        if rows[3] != headers:
            return False

        for row in rows[4:]:
            if not isinstance(row, list) or len(row) != len(headers):
                return False
            if any(not str(value).strip() for value in row[: min(3, len(row))]):
                return False

        return True

    def add_support_rows(self, rows):
        table_type = self.extract_table_type(rows)

        rows.extend([[], ["表格使用说明", "内容"]])
        rows.extend(self.build_usage_rows(table_type))

        rows.extend([[], ["数据填写规则", "说明"]])
        rows.extend(self.build_data_rule_rows(table_type))

        rows.extend([[], ["推荐分析图表", "适用场景"]])
        rows.extend(self.build_chart_rows(table_type))

        rows.extend([[], ["质量检查清单", "检查要求"]])
        rows.extend(self.build_quality_check_rows(table_type))

        rows.extend([[], ["字段说明", "内容"]])
        rows.extend(self.build_field_note_rows(table_type))

        return rows

    def extract_table_type(self, rows):
        for row in rows:
            if len(row) >= 2 and row[0] == "表格类型":
                return row[1]
        return "通用表格"

    def build_usage_rows(self, table_type):
        return [
            ["使用说明", f"这是一份{table_type}，用于记录和整理当前办公数据。"],
            ["使用说明", "表格已经包含可直接查看的业务记录和辅助说明。"],
            ["使用说明", "后续分析可以基于推荐图表生成看板或汇报材料。"],
        ]

    def build_data_rule_rows(self, table_type):
        common_rules = [
            ["规则", "不要删除表头，新增字段请放在现有字段右侧。"],
            ["规则", "日期、金额、状态、负责人等字段要保持格式一致。"],
            ["规则", "不确定的信息先写入备注，不要混入主要数据列。"],
        ]

        if table_type == "客户信息表":
            return common_rules + [
                ["规则", "客户名称不要重复，电话和联系人缺失时必须在备注中说明。"],
                ["规则", "跟进状态固定为：待跟进、跟进中、已成交、已流失。"],
            ]

        if table_type == "销售报表":
            return common_rules + [
                ["规则", "销售额、成本、利润必须使用数字，不要写入单位文字。"],
                ["规则", "利润按销售额减成本计算，异常值要单独标注。"],
            ]

        if table_type == "数据统计表":
            return common_rules + [
                ["规则", "数值列只填写数字，文字说明放入备注列。"],
                ["规则", "合计行需要和明细数据保持一致。"],
            ]

        return common_rules

    def build_chart_rows(self, table_type):
        if table_type == "客户信息表":
            return [
                ["柱状图", "统计不同跟进状态下的客户数量。"],
                ["饼图", "查看客户状态占比。"],
                ["明细表", "筛选待跟进客户，方便安排下一步动作。"],
            ]

        if table_type == "销售报表":
            return [
                ["折线图", "查看销售额随日期变化的趋势。"],
                ["柱状图", "对比不同产品的销售额、成本和利润。"],
                ["排行榜", "找出贡献最高的产品或业务项。"],
            ]

        if table_type == "数据统计表":
            return [
                ["柱状图", "对比不同项目的数值大小。"],
                ["折线图", "如果数据有时间顺序，用于观察趋势。"],
                ["异常值标记", "找出明显偏高或偏低的数据。"],
            ]

        return [
            ["柱状图", "对比不同事项或分类的数量。"],
            ["状态统计", "统计未开始、进行中、已完成事项。"],
            ["明细表", "保留原始记录，方便后续检查。"],
        ]

    def build_quality_check_rows(self, table_type):
        return [
            ["检查", "表格主题是否清晰。"],
            ["检查", f"{table_type} 的表头是否和实际业务一致。"],
            ["检查", "关键业务数据是否已经补充完整。"],
            ["检查", "关键字段是否存在空值、重复值或格式混乱。"],
            ["检查", "推荐图表是否能支撑最终要表达的结论。"],
        ]

    def build_field_note_rows(self, table_type):
        if table_type == "客户信息表":
            return [
                ["字段说明", "客户名称用于识别客户主体。"],
                ["字段说明", "跟进状态用于区分待跟进、跟进中、已成交和已流失。"],
                ["字段说明", "备注用于记录沟通结果和下一次行动。"],
            ]

        if table_type == "销售报表":
            return [
                ["字段说明", "销售额、成本和利润均使用数字记录。"],
                ["字段说明", "利润等于销售额减成本。"],
                ["字段说明", "备注用于记录利润率或异常原因。"],
            ]

        if table_type == "数据统计表":
            return [
                ["字段说明", "项目列记录统计对象。"],
                ["字段说明", "数值列记录可计算的数据。"],
                ["字段说明", "备注列解释数据口径和业务含义。"],
            ]

        return [
            ["字段说明", "事项列记录具体任务。"],
            ["字段说明", "负责人列记录主要执行人。"],
            ["字段说明", "状态列用于跟踪未开始、进行中和已完成。"],
        ]

    def extract_table_topic(self, user_task):
        cleaned_topic = user_task
        removable_words = [
            "帮我",
            "生成",
            "整理",
            "做一份",
            "写一份",
            "Excel 表格",
            "excel 表格",
            "Excel",
            "excel",
            "表格",
        ]

        for word in removable_words:
            cleaned_topic = cleaned_topic.replace(word, "")

        cleaned_topic = cleaned_topic.strip(" ：:，。")
        return cleaned_topic or "办公数据"

    def detect_table_type(self, user_task):
        if "客户" in user_task:
            return "客户信息表"

        if "销售" in user_task or "营收" in user_task or "收入" in user_task:
            return "销售报表"

        if "统计" in user_task or "数据" in user_task or "计算" in user_task:
            return "数据统计表"

        return "通用表格"

    def write_xlsx(self, table_path, rows):
        with ZipFile(table_path, "w", ZIP_DEFLATED) as xlsx_file:
            xlsx_file.writestr("[Content_Types].xml", self.build_content_types_xml())
            xlsx_file.writestr("_rels/.rels", self.build_root_relationships_xml())
            xlsx_file.writestr("xl/workbook.xml", self.build_workbook_xml())
            xlsx_file.writestr("xl/_rels/workbook.xml.rels", self.build_workbook_relationships_xml())
            xlsx_file.writestr("xl/styles.xml", self.build_styles_xml())
            xlsx_file.writestr("xl/worksheets/sheet1.xml", self.build_sheet_xml(rows))

    def build_sheet_xml(self, rows):
        row_xml_list = []
        for row_index, row in enumerate(rows, start=1):
            cell_xml_list = []
            for column_index, value in enumerate(row, start=1):
                cell_name = f"{self.column_name(column_index)}{row_index}"
                style_index = self.detect_cell_style(row_index, value)
                cell_xml_list.append(self.build_text_cell_xml(cell_name, value, style_index))

            row_xml_list.append(f'<row r="{row_index}">{"".join(cell_xml_list)}</row>')

        rows_xml = "".join(row_xml_list)
        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
            "<cols>"
            '<col min="1" max="1" width="16" customWidth="1"/>'
            '<col min="2" max="6" width="18" customWidth="1"/>'
            "</cols>"
            f"<sheetData>{rows_xml}</sheetData>"
            "</worksheet>"
        )

    def build_text_cell_xml(self, cell_name, value, style_index):
        safe_value = escape(str(value))
        return (
            f'<c r="{cell_name}" t="inlineStr" s="{style_index}">'
            f"<is><t>{safe_value}</t></is>"
            "</c>"
        )

    def detect_cell_style(self, row_index, value):
        if row_index == 1:
            return 1

        if str(value) in ["项目", "客户名称", "日期", "序号"]:
            return 2

        return 0

    def column_name(self, column_index):
        name = ""
        while column_index:
            column_index, remainder = divmod(column_index - 1, 26)
            name = chr(65 + remainder) + name
        return name

    def build_content_types_xml(self):
        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
            '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
            '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
            "</Types>"
        )

    def build_root_relationships_xml(self):
        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
            "</Relationships>"
        )

    def build_workbook_xml(self):
        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
            "<sheets>"
            '<sheet name="办公表格" sheetId="1" r:id="rId1"/>'
            "</sheets>"
            "</workbook>"
        )

    def build_workbook_relationships_xml(self):
        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>'
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
            "</Relationships>"
        )

    def build_styles_xml(self):
        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
            "<fonts count=\"2\">"
            '<font><sz val="11"/><name val="Calibri"/></font>'
            '<font><b/><sz val="11"/><name val="Calibri"/></font>'
            "</fonts>"
            '<fills count="2"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill></fills>'
            '<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>'
            '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
            '<cellXfs count="3">'
            '<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>'
            '<xf numFmtId="0" fontId="1" fillId="0" borderId="0" xfId="0" applyFont="1"/>'
            '<xf numFmtId="0" fontId="1" fillId="0" borderId="0" xfId="0" applyFont="1"/>'
            "</cellXfs>"
            "</styleSheet>"
        )
