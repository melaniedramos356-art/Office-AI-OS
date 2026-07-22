from agents.data_analysis_inspiration_library import DataAnalysisInspirationLibrary
from agents.file_reader_agent import FileReaderAgent
from agents.inspiration_library import InspirationLibrary
from agents.production_technique_library import ProductionTechniqueLibrary
from agents.qa_agent import QAAgent


class FileImprovementAgent:
    def __init__(self):
        self.file_reader_agent = FileReaderAgent()
        self.inspiration_library = InspirationLibrary()
        self.data_analysis_inspiration_library = DataAnalysisInspirationLibrary()
        self.production_technique_library = ProductionTechniqueLibrary()
        self.qa_agent = QAAgent()

    def handle(self, user_task):
        if not isinstance(user_task, str) or not user_task.strip():
            return "File Improvement Agent 没有收到有效任务。"

        file_path = self.file_reader_agent.extract_file_path(user_task)
        if not file_path:
            return "File Improvement Agent 没有找到文件路径，请提供要改进的 .docx、.pptx 或 .xlsx 文件路径。"

        if not file_path.exists():
            return f"File Improvement Agent 没有找到文件：{file_path}"

        if file_path.suffix.lower() not in [".docx", ".pptx", ".xlsx"]:
            return f"File Improvement Agent 暂只支持改进 Word、PPT、Excel 文件：{file_path.suffix}"

        try:
            file_content = self.qa_agent.read_file_content(file_path)
        except OSError as error:
            return f"File Improvement Agent 读取文件失败：{error}"

        file_type = self.detect_file_type(file_path)
        section_name = self.detect_section_name(file_path)

        return (
            "File Improvement Agent 已生成文件改进建议。\n"
            f"任务内容：{user_task.strip()}\n"
            f"文件位置：{file_path}\n"
            f"文件类型：{file_type}\n"
            f"字符数量：{len(file_content)}\n\n"
            "## 当前内容判断\n"
            f"{self.build_content_review(file_content)}\n\n"
            "## 制作技巧建议\n"
            f"{self.build_technique_text(section_name)}\n\n"
            "## 分项改进建议\n"
            f"{self.build_improvement_text(section_name)}\n\n"
            "## 素材与灵感来源\n"
            f"{self.build_source_text(section_name, user_task)}\n\n"
            "## 下一步执行\n"
            f"{self.build_next_step(section_name)}"
        )

    def detect_file_type(self, file_path):
        suffix_map = {
            ".docx": "Word 文档",
            ".pptx": "PPT 演示稿",
            ".xlsx": "Excel 表格",
        }
        return suffix_map.get(file_path.suffix.lower(), "未知文件")

    def detect_section_name(self, file_path):
        suffix_map = {
            ".docx": "word",
            ".pptx": "ppt",
            ".xlsx": "excel",
        }
        return suffix_map.get(file_path.suffix.lower(), "shared")

    def build_content_review(self, file_content):
        if not isinstance(file_content, str) or not file_content.strip():
            return "- 文件内容为空，建议先检查文件是否损坏。"

        lines = [line.strip() for line in file_content.splitlines() if line.strip()]
        review_items = [
            f"- 已读取到 {len(lines)} 行有效文本。",
            "- 建议先确认核心目标、目标读者和最终交付场景。",
        ]

        if len(lines) < 6:
            review_items.append("- 当前内容偏少，建议补充背景、结论、数据或案例。")
        else:
            review_items.append("- 当前内容具备继续优化基础，可以进入结构、语言和视觉改进。")

        return "\n".join(review_items)

    def build_technique_text(self, section_name):
        techniques = self.production_technique_library.get_techniques(section_name)
        return "\n".join([f"- {technique}" for technique in techniques[:6]])

    def build_improvement_text(self, section_name):
        advice_map = {
            "word": [
                "文案修改：先压缩重复表达，再补充结论、依据和下一步动作。",
                "语言丰富：把空泛描述改成具体时间、对象、数据和结果。",
                "版面设计：统一标题层级，长段落拆成短段落或项目符号。",
                "图片建议：优先补充流程图、成果截图、业务场景图。",
            ],
            "ppt": [
                "版面设计：每页只保留一个核心观点，减少大段文字。",
                "文案修改：把页面标题改成结论式标题，而不是普通名词。",
                "图片建议：为封面、核心观点页、数据页分别找不同素材。",
                "视觉节奏：交替使用结论页、图表页、案例页，避免页面单调。",
            ],
            "excel": [
                "数据规则：检查空值、重复值、异常值和字段格式。",
                "图表建议：按趋势、对比、占比、异常四类问题选择图表。",
                "分析建议：先明确指标口径，再做汇总、排序和筛选。",
                "版面设计：把原始数据、分析结果、图表建议分区摆放。",
            ],
        }
        advice = advice_map.get(section_name, ["先整理结构，再优化内容，最后检查输出质量。"])
        return "\n".join([f"- {item}" for item in advice])

    def build_source_text(self, section_name, user_task):
        if section_name == "excel":
            rows = self.data_analysis_inspiration_library.build_source_rows(user_task, limit=4)
            return "\n".join([f"- {row[0]}：{row[3]}（{row[2]}）" for row in rows])

        return "\n".join(self.inspiration_library.build_source_lines(user_task, limit=4))

    def build_next_step(self, section_name):
        next_step_map = {
            "word": "- 下一步可以交给 Word Agent 生成一个结构更清楚、语言更丰富的改进版文档。",
            "ppt": "- 下一步可以交给 PPT Agent 生成一个有目录、结构建议、图片建议的改进版演示稿。",
            "excel": "- 下一步可以交给 Excel Agent 生成一个带填写规则、图表建议和质量清单的改进版表格。",
        }
        return next_step_map.get(section_name, "- 下一步交给 AI Butler Agent 继续拆解任务。")
