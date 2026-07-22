from agents.data_analysis_inspiration_library import DataAnalysisInspirationLibrary
from agents.file_reader_agent import FileReaderAgent
from agents.inspiration_library import InspirationLibrary
from agents.production_technique_library import ProductionTechniqueLibrary
from agents.qa_agent import QAAgent
from agents.ppt_agent import PPTAgent
from agents.word_agent import WordAgent
from agents.excel_agent import ExcelAgent


class FileImprovementAgent:
    def __init__(self):
        self.file_reader_agent = FileReaderAgent()
        self.inspiration_library = InspirationLibrary()
        self.data_analysis_inspiration_library = DataAnalysisInspirationLibrary()
        self.production_technique_library = ProductionTechniqueLibrary()
        self.qa_agent = QAAgent()
        self.ppt_agent = PPTAgent(output_folder="outputs/improved_ppt_files")
        self.word_agent = WordAgent(output_folder="outputs/improved_word_documents")
        self.excel_agent = ExcelAgent(output_folder="outputs/improved_excel_files")

    def handle(self, user_task):
        if not isinstance(user_task, str) or not user_task.strip():
            return "File Improvement Agent 没有收到有效任务。"

        if self.should_create_improved_file(user_task):
            return self.create_improved_word_document(user_task)

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

    def should_create_improved_file(self, user_task):
        create_keywords = ["生成改进版", "生成修改版", "输出改进版", "制作改进版"]
        for keyword in create_keywords:
            if keyword in user_task:
                return True
        return False

    def create_improved_word_document(self, user_task):
        if not isinstance(user_task, str) or not user_task.strip():
            return "File Improvement Agent 没有收到有效任务。"

        file_path = self.file_reader_agent.extract_file_path(user_task)
        if not file_path:
            return "File Improvement Agent 没有找到文件路径。"

        if not file_path.exists():
            return f"File Improvement Agent 没有找到文件：{file_path}"

        try:
            file_content = self.qa_agent.read_file_content(file_path)
        except OSError as error:
            return f"File Improvement Agent 读取文件失败：{error}"

        if file_path.suffix.lower() == ".pptx":
            return self.create_improved_ppt_file(user_task, file_path, file_content)

        if file_path.suffix.lower() == ".xlsx":
            return self.create_improved_excel_file(user_task, file_path, file_content)

        if file_path.suffix.lower() != ".docx":
            return "File Improvement Agent 当前只支持生成 Word、PPT、Excel 改进版文件。"

        paragraphs = self.build_improved_word_paragraphs(file_path, file_content)
        output_path = self.word_agent.output_folder / self.word_agent.build_file_name()
        self.word_agent.output_folder.mkdir(parents=True, exist_ok=True)
        self.word_agent.write_docx(output_path, paragraphs)

        return (
            "File Improvement Agent 已生成 Word 改进版文件。\n"
            f"任务内容：{user_task.strip()}\n"
            f"原文件位置：{file_path}\n"
            f"文件位置：{output_path}"
        )

    def create_improved_ppt_file(self, user_task, file_path, file_content):
        slides = self.build_improved_ppt_slides(file_path, file_content)
        output_path = self.ppt_agent.output_folder / self.ppt_agent.build_file_name()
        self.ppt_agent.output_folder.mkdir(parents=True, exist_ok=True)
        self.ppt_agent.write_pptx(output_path, slides)

        return (
            "File Improvement Agent 已生成 PPT 改进版文件。\n"
            f"任务内容：{user_task.strip()}\n"
            f"原文件位置：{file_path}\n"
            f"文件位置：{output_path}"
        )

    def create_improved_excel_file(self, user_task, file_path, file_content):
        rows = self.build_improved_excel_rows(file_path, file_content)
        output_path = self.excel_agent.output_folder / self.excel_agent.build_file_name()
        self.excel_agent.output_folder.mkdir(parents=True, exist_ok=True)
        self.excel_agent.write_xlsx(output_path, rows)

        return (
            "File Improvement Agent 已生成 Excel 改进版文件。\n"
            f"任务内容：{user_task.strip()}\n"
            f"原文件位置：{file_path}\n"
            f"文件位置：{output_path}"
        )

    def build_improved_word_paragraphs(self, file_path, file_content):
        original_lines = [line.strip() for line in file_content.splitlines() if line.strip()]
        preview_lines = original_lines[:8]

        paragraphs = [
            ("title", "Word 改进版文档"),
            ("heading", "原文件位置"),
            ("text", str(file_path)),
            ("heading", "改进摘要"),
            ("text", "本文件基于原 Word 内容生成，重点增强结构、文案表达、版面层级和图片素材建议。"),
            ("heading", "原文内容摘录"),
        ]

        for line in preview_lines:
            paragraphs.append(("bullet", line[:160]))

        paragraphs.extend(
            [
                ("heading", "结构优化建议"),
                ("bullet", "先补充核心结论，再展开背景、依据和下一步动作。"),
                ("bullet", "把长段落拆成短段落或项目符号，提升可读性。"),
                ("bullet", "统一标题层级，避免同一级标题表达不同信息层次。"),
                ("heading", "文案润色方向"),
                ("bullet", "把空泛描述改成具体对象、时间、数据和结果。"),
                ("bullet", "减少重复表达，保留最能支撑结论的信息。"),
                ("bullet", "重要结论前置，说明和补充内容后置。"),
                ("heading", "版面设计方向"),
                ("bullet", "标题、正文、备注使用不同层级，保持留白和对齐。"),
                ("bullet", "关键结论后预留截图、流程图或案例图片位置。"),
                ("heading", "图片素材建议"),
            ]
        )

        for source_line in self.inspiration_library.build_source_lines(str(file_path), limit=4):
            paragraphs.append(("bullet", source_line.replace("- ", "", 1)))

        paragraphs.extend(
            [
                ("heading", "待人工确认"),
                ("bullet", "请确认原文中的真实数据、人员、时间和业务背景是否完整。"),
                ("bullet", "请确认是否需要继续生成正式可交付版本。"),
            ]
        )

        return paragraphs

    def build_improved_ppt_slides(self, file_path, file_content):
        original_lines = [line.strip() for line in file_content.splitlines() if line.strip()]
        preview_lines = original_lines[:5]

        return [
            {
                "title": "PPT 改进版",
                "bullets": [
                    f"原文件：{file_path}",
                    "目标：优化页面结构、版面层级、文案表达和图片素材建议",
                    "说明：本文件不会覆盖原 PPT",
                ],
            },
            {
                "title": "原文件内容摘录",
                "bullets": preview_lines or ["原文件没有读取到有效文本"],
            },
            {
                "title": "页面结构优化",
                "bullets": [
                    "用目录页明确整体叙事顺序",
                    "每页只保留一个核心观点",
                    "把长句改成 3 条以内的短要点",
                ],
            },
            {
                "title": "结论式标题建议",
                "bullets": [
                    "标题直接表达本页结论",
                    "避免只写背景、问题、方案这类空标题",
                    "关键页优先突出数据、变化或行动",
                ],
            },
            {
                "title": "版面设计建议",
                "bullets": [
                    "保持标题、正文、备注区域对齐",
                    "每页预留图片或图表区域",
                    "同类页面使用一致的字号和布局",
                ],
            },
            {
                "title": "图片素材建议",
                "bullets": self.build_ppt_source_bullets(str(file_path)),
            },
        ]

    def build_ppt_source_bullets(self, user_task):
        source_lines = self.inspiration_library.build_source_lines(user_task, limit=4)
        bullets = [source_line.replace("- ", "", 1) for source_line in source_lines]
        bullets.extend(
            [
                "搜索词：商务汇报 版式 灵感",
                "搜索词：项目汇报 流程图 数据可视化",
            ]
        )
        return bullets

    def build_improved_excel_rows(self, file_path, file_content):
        original_lines = [line.strip() for line in file_content.splitlines() if line.strip()]
        preview_lines = original_lines[:8]

        rows = [
            ["Excel 改进版", ""],
            ["原文件位置", str(file_path)],
            ["改进目标", "优化字段结构、数据规则、分析图表和质量检查"],
            [],
            ["原数据摘录", "内容"],
        ]

        if preview_lines:
            for index, line in enumerate(preview_lines, start=1):
                rows.append([f"摘录 {index}", line[:160]])
        else:
            rows.append(["摘录", "原文件没有读取到有效文本"])

        rows.extend(
            [
                [],
                ["字段检查", "建议"],
                ["字段检查", "确认表头是否稳定，避免一列混合多种含义。"],
                ["字段检查", "日期、金额、状态等字段要保持统一格式。"],
                ["字段检查", "不确定信息放入备注列，不要污染主要数据列。"],
                [],
                ["数据填写规则", "说明"],
                ["规则", "先替换示例数据，再补充真实业务信息。"],
                ["规则", "检查空值、重复值、异常值和格式混乱。"],
                ["规则", "保留原始需求和数据来源，方便后续追溯。"],
                [],
                ["推荐分析图表", "适用场景"],
                ["折线图", "适合查看趋势变化。"],
                ["柱状图", "适合对比不同分类或对象。"],
                ["饼图", "适合查看占比结构。"],
                ["排行榜", "适合找出贡献最高或最低的项目。"],
                [],
                ["数据分析网站灵感库", "类型", "用途", "链接"],
            ]
        )

        rows.extend(self.data_analysis_inspiration_library.build_source_rows(str(file_path), limit=6))

        rows.extend(
            [
                [],
                ["质量检查清单", "检查要求"],
                ["检查", "原数据是否已经保留。"],
                ["检查", "关键字段是否存在空值或重复。"],
                ["检查", "推荐图表是否能支撑最终结论。"],
                ["检查", "是否需要继续生成正式分析看板。"],
            ]
        )

        return rows
