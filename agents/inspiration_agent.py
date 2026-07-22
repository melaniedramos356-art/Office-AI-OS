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
