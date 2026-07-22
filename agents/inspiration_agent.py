from datetime import datetime
from pathlib import Path

from agents.china_inspiration_library import ChinaInspirationLibrary
from agents.data_analysis_inspiration_library import DataAnalysisInspirationLibrary
from agents.inspiration_library import InspirationLibrary
from agents.production_technique_library import ProductionTechniqueLibrary


class InspirationAgent:
    def __init__(self, output_folder="outputs/inspiration_plans"):
        self.output_folder = Path(output_folder)
        self.inspiration_library = InspirationLibrary()
        self.china_inspiration_library = ChinaInspirationLibrary()
        self.data_analysis_inspiration_library = DataAnalysisInspirationLibrary()
        self.production_technique_library = ProductionTechniqueLibrary()

    def handle(self, user_task):
        if not isinstance(user_task, str) or not user_task.strip():
            return "Inspiration Agent 没有收到有效任务。"

        cleaned_task = user_task.strip()

        try:
            plan_path = self.create_plan(cleaned_task)
        except OSError as error:
            return f"Inspiration Agent 创建灵感计划失败：{error}"

        return (
            "Inspiration Agent 已生成素材灵感计划。\n"
            f"任务内容：{cleaned_task}\n"
            f"文件位置：{plan_path}"
        )

    def create_plan(self, user_task):
        self.output_folder.mkdir(parents=True, exist_ok=True)
        plan_path = self.output_folder / self.build_file_name()
        plan_path.write_text(self.build_plan_content(user_task), encoding="utf-8")
        return plan_path

    def build_file_name(self):
        time_text = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        return f"inspiration_plan_{time_text}.md"

    def build_plan_content(self, user_task):
        section_name = self.detect_section_name(user_task)
        source_text = self.build_source_text(section_name, user_task)
        keyword_text = self.build_keyword_text(section_name, user_task)
        technique_text = self.build_technique_text(section_name)
        visual_text = self.build_visual_text(section_name, user_task)
        layout_text = self.build_layout_text(section_name)
        handoff_text = self.build_handoff_text(section_name, user_task)
        action_text = self.build_action_text(section_name)

        return (
            "# 素材灵感计划\n\n"
            f"## 原始需求\n\n{user_task}\n\n"
            f"## 任务类型\n\n{section_name}\n\n"
            "## 优先查找网站\n\n"
            f"{source_text}\n\n"
            "## 建议搜索词\n\n"
            f"{keyword_text}\n\n"
            "## 可复用制作技巧\n\n"
            f"{technique_text}\n\n"
            "## 图片查找与生成建议\n\n"
            f"{visual_text}\n\n"
            "## 版面参考重点\n\n"
            f"{layout_text}\n\n"
            "## 交给生成 Agent 的指令\n\n"
            f"{handoff_text}\n\n"
            "## 落地动作\n\n"
            f"{action_text}\n\n"
            "## 注意事项\n\n"
            "- 只把网站作为灵感来源，不直接照抄他人作品。\n"
            "- 记录素材来源、关键词和用途，方便后续追溯。\n"
            "- 生成 Word / PPT / Excel 前，先确认最终读者和交付场景。\n"
        )

    def detect_section_name(self, user_task):
        task_text = user_task.lower()

        if "excel" in task_text or "表格" in user_task or "数据" in user_task:
            return "excel"

        if "ppt" in task_text or "幻灯片" in user_task or "汇报" in user_task:
            return "ppt"

        if "word" in task_text or "文档" in user_task or "报告" in user_task:
            return "word"

        return "shared"

    def build_source_text(self, section_name, user_task):
        if section_name == "excel":
            rows = self.data_analysis_inspiration_library.build_source_rows(user_task, limit=6)
            return "\n".join([f"- {row[0]}：{row[3]}（{row[2]}）" for row in rows])

        international_lines = self.inspiration_library.build_source_lines(user_task, limit=5)
        china_lines = self.china_inspiration_library.build_source_lines(user_task, limit=5)
        return "\n".join(international_lines + china_lines)

    def build_keyword_text(self, section_name, user_task):
        if section_name == "excel":
            rows = self.data_analysis_inspiration_library.build_keyword_rows(user_task)
            return "\n".join([f"- {row[1]}" for row in rows])

        keywords = (
            self.inspiration_library.build_search_keywords(user_task)
            + self.china_inspiration_library.build_search_keywords(user_task)
        )
        return "\n".join([f"- {keyword}" for keyword in self.unique_items(keywords)])

    def build_technique_text(self, section_name):
        techniques = self.production_technique_library.get_techniques(section_name)
        return "\n".join([f"- {technique}" for technique in techniques])

    def build_visual_text(self, section_name, user_task):
        visual_map = {
            "word": [
                f"图片查找关键词：{user_task} 流程图",
                f"图片查找关键词：{user_task} 业务场景图",
                "图片生成提示词：中文办公报告，真实业务场景，干净背景，适合插入 Word 文档。",
                "使用位置：摘要后、关键结论后、流程说明处。",
            ],
            "ppt": [
                f"图片查找关键词：{user_task} 封面设计",
                f"图片查找关键词：{user_task} 活动视觉",
                "图片生成提示词：中文商务 PPT 封面，清晰主体，高级感，留出标题区域，16:9。",
                "使用位置：封面页、章节页、核心观点页、结尾页。",
            ],
            "excel": [
                f"图片查找关键词：{user_task} 数据看板",
                f"图片查找关键词：{user_task} dashboard examples",
                "图片生成提示词：现代数据分析看板，清晰图表，浅色背景，适合 Excel 分析页参考。",
                "使用位置：图表建议页、分析说明页、汇报截图页。",
            ],
            "shared": [
                f"图片查找关键词：{user_task} 办公设计",
                f"图片查找关键词：{user_task} 案例参考",
                "图片生成提示词：中文办公场景，清晰信息层级，干净专业，适合文档或演示使用。",
                "使用位置：先根据最终文件类型决定。",
            ],
        }
        return "\n".join([f"- {item}" for item in visual_map[section_name]])

    def build_layout_text(self, section_name):
        layout_map = {
            "word": [
                "标题层级：一级标题说明主题，二级标题说明具体内容。",
                "段落节奏：长段落拆成短段落或项目符号。",
                "信息顺序：结论、依据、案例、下一步。",
            ],
            "ppt": [
                "页面结构：每页一个核心观点，不堆长段文字。",
                "视觉区域：封面、目录、数据页、结论页使用不同版式。",
                "重点表达：标题尽量写成结论句。",
            ],
            "excel": [
                "表格结构：原始数据、分析结果、图表建议分区放置。",
                "图表选择：趋势用折线，对比用柱状，占比用饼图，异常用标记。",
                "字段设计：日期、金额、分类、备注等字段保持格式稳定。",
            ],
            "shared": [
                "先判断最终文件类型，再选择 Word、PPT 或 Excel 的版面规则。",
                "所有素材都要服务核心信息，不只看装饰效果。",
                "同一份文件保持字体、颜色和信息层级一致。",
            ],
        }
        return "\n".join([f"- {item}" for item in layout_map[section_name]])

    def build_handoff_text(self, section_name, user_task):
        agent_map = {
            "word": "Word Agent",
            "ppt": "PPT Agent",
            "excel": "Excel Agent",
            "shared": "AI Butler Agent",
        }
        agent_name = agent_map[section_name]
        return (
            f"- 交给 {agent_name}：{user_task}\n"
            "- 生成时参考本计划中的网站、搜索词、制作技巧和版面重点。\n"
            "- 如果是修改已有文件，先交给 File Reader Agent 读取原文件，再交给 File Improvement Agent。"
        )

    def build_action_text(self, section_name):
        action_map = {
            "word": [
                "先整理标题层级和段落结构。",
                "再用灵感来源补充案例、流程图或场景图片建议。",
                "最后交给 Word Agent 生成正式文档。",
            ],
            "ppt": [
                "先确定每页只讲一个核心观点。",
                "再从灵感网站找封面、目录、数据页和结论页参考。",
                "最后交给 PPT Agent 生成演示稿。",
            ],
            "excel": [
                "先确认字段、口径和数据来源。",
                "再参考数据分析网站选择趋势、对比、占比或异常图表。",
                "最后交给 Excel Agent 生成表格或分析草稿。",
            ],
            "shared": [
                "先判断最终要生成 Word、PPT 还是 Excel。",
                "再按对应类型查找素材和制作技巧。",
                "最后交给对应 Agent 生成文件。",
            ],
        }
        return "\n".join([f"{index + 1}. {action}" for index, action in enumerate(action_map[section_name])])

    def unique_items(self, items):
        unique_values = []
        for item in items:
            if item not in unique_values:
                unique_values.append(item)
        return unique_values
