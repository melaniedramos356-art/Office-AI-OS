from agents.data_analysis_inspiration_library import DataAnalysisInspirationLibrary
from agents.china_inspiration_library import ChinaInspirationLibrary
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
        self.china_inspiration_library = ChinaInspirationLibrary()
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

        source_lines = self.inspiration_library.build_source_lines(user_task, limit=4)
        china_source_lines = self.china_inspiration_library.build_source_lines(user_task, limit=4)
        return "\n".join(source_lines + china_source_lines)

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
        topic = self.build_improved_topic(file_path, original_lines)
        content_context = self.build_content_context(original_lines)

        return [
            ("title", f"{topic}（改进版）"),
            ("heading", "一、核心摘要"),
            ("text", f"本文件围绕“{topic}”重新组织内容，突出主题、结论、依据和行动安排。改进版弱化零散说明，强化读者能够直接理解的完整表达，使文档更适合正式阅读、汇报流转和后续归档。"),
            ("heading", "二、内容基础"),
            ("text", content_context),
            ("heading", "三、重点表达"),
            ("text", "从现有内容看，文档应优先呈现最关键的结论，再展开背景、过程和支撑信息。表达上要减少重复铺垫，把抽象描述转化为具体对象、具体动作和具体结果，让读者在较短时间内把握文件重点。"),
            ("heading", "四、执行安排"),
            ("text", "后续推进应围绕目标、责任、时间和质量四个方面展开：目标上明确最终交付物，责任上对应到具体执行主体，时间上形成可检查节点，质量上保留关键依据和过程记录，保证文档内容能够支撑实际工作。"),
            ("heading", "五、结语"),
            ("text", "总体来看，改进版文档以清晰结构承接原有内容，以更完整的语言呈现核心信息。全文围绕主题、依据、行动和结果展开，能够作为正式沟通、阶段汇报或内部归档的基础文件使用。"),
        ]

    def build_improved_ppt_slides(self, file_path, file_content):
        original_lines = [line.strip() for line in file_content.splitlines() if line.strip()]
        topic = self.build_improved_topic(file_path, original_lines)
        preview_lines = self.build_short_points(original_lines, limit=3)

        return [
            {
                "title": f"{topic}改进版汇报",
                "bullets": [
                    "围绕原文件内容重新组织汇报逻辑",
                    "用结论式标题提升页面表达效率",
                    "适合用于正式汇报前的二次打磨",
                ],
            },
            {
                "title": "核心信息已经完成重新梳理",
                "bullets": preview_lines,
            },
            {
                "title": "汇报主线从信息罗列转向结论表达",
                "bullets": [
                    "先说明核心判断，再补充背景和依据",
                    "每页只保留一个主要观点",
                    "用短句承载重点，减少大段文字",
                ],
            },
            {
                "title": "关键页面需要突出事实、变化和行动",
                "bullets": [
                    "事实页说明当前基础和已完成内容",
                    "问题页说明影响范围和处理优先级",
                    "行动页说明责任、节点和交付标准",
                ],
            },
            {
                "title": "视觉呈现围绕阅读效率展开",
                "bullets": [
                    "标题区承载结论，正文区承载依据",
                    "同类页面保持一致字号和对齐方式",
                    "图表、截图和流程图只用于支撑观点",
                ],
            },
            {
                "title": "后续落地聚焦可执行事项",
                "bullets": [
                    "用真实数据、案例或现场图片支撑页面观点",
                    "统一页面风格并检查文字是否过密",
                    "按汇报场景调整讲述顺序和重点",
                ],
            },
        ]

    def build_ppt_source_bullets(self, user_task):
        source_lines = self.inspiration_library.build_source_lines(user_task, limit=4)
        china_source_lines = self.china_inspiration_library.build_source_lines(user_task, limit=4)
        bullets = [source_line.replace("- ", "", 1) for source_line in source_lines + china_source_lines]
        bullets.extend(
            [
                "搜索词：商务汇报 版式 灵感",
                "搜索词：项目汇报 流程图 数据可视化",
            ]
        )
        return bullets

    def build_improved_excel_rows(self, file_path, file_content):
        original_lines = [line.strip() for line in file_content.splitlines() if line.strip()]
        topic = self.build_improved_topic(file_path, original_lines)
        preview_lines = self.build_short_points(original_lines, limit=6)

        rows = [
            ["Excel 改进版分析表", ""],
            ["分析主题", topic],
            ["改进目标", "形成可阅读、可检查、可继续分析的数据文件"],
            [],
            ["核心信息重组", "内容"],
        ]

        for index, line in enumerate(preview_lines, start=1):
            rows.append([f"信息 {index}", line])

        rows.extend(
            [
                [],
                ["分析结论", "内容"],
                ["结论", "当前数据文件应先明确主题、字段含义和后续分析目标。"],
                ["结论", "关键信息需要拆成稳定字段，避免一列混合多个含义。"],
                ["结论", "后续汇报应围绕趋势、对比、占比或异常展开。"],
                [],
                ["字段规范", "说明"],
                ["规则", "主题、日期、对象、数值、状态和备注应分列记录。"],
                ["规则", "日期、金额、数量等字段保持统一格式。"],
                ["规则", "异常值和缺失值单独标注原因，方便复盘。"],
                [],
                ["推荐分析图表", "适用场景"],
                ["折线图", "适合查看趋势变化。"],
                ["柱状图", "适合对比不同分类或对象。"],
                ["饼图", "适合查看占比结构。"],
                ["排行榜", "适合找出贡献最高或最低的项目。"],
                [],
                ["数据看板结构", "内容"],
                ["顶部指标", "展示核心数值、变化幅度和完成情况。"],
                ["中部图表", "展示趋势、对比和结构。"],
                ["底部明细", "保留原始记录和异常说明。"],
            ]
        )

        rows.extend(
            [
                [],
                ["质量检查清单", "检查要求"],
                ["检查", "主题是否清晰。"],
                ["检查", "关键字段是否存在空值或重复。"],
                ["检查", "推荐图表是否能支撑最终结论。"],
                ["检查", "明细数据是否便于后续追溯。"],
            ]
        )

        return rows

    def build_improved_topic(self, file_path, original_lines):
        for line in original_lines:
            cleaned_line = line.strip(" ：:，。")
            if 2 <= len(cleaned_line) <= 40:
                return cleaned_line

        return file_path.stem or "办公文件"

    def build_content_context(self, original_lines):
        points = self.build_short_points(original_lines, limit=5)
        if not points:
            return "原文件有效内容较少，改进版已按通用办公文件结构补充主题、重点表达、执行安排和结语。"

        return "；".join(points) + "。"

    def build_short_points(self, original_lines, limit=5):
        points = []
        for line in original_lines:
            cleaned_line = " ".join(line.strip().split())
            if not cleaned_line:
                continue
            points.append(cleaned_line[:80])
            if len(points) >= limit:
                break

        return points or ["原文件有效内容较少，需要围绕主题、重点、结论和行动重新组织。"]
