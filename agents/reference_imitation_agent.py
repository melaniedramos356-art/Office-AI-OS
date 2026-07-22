from agents.excel_agent import ExcelAgent
from agents.file_reader_agent import FileReaderAgent
from agents.ppt_agent import PPTAgent
from agents.qa_agent import QAAgent
from agents.word_agent import WordAgent


class ReferenceImitationAgent:
    def __init__(self):
        self.file_reader_agent = FileReaderAgent()
        self.qa_agent = QAAgent()
        self.word_agent = WordAgent(output_folder="outputs/reference_word_documents")
        self.ppt_agent = PPTAgent(output_folder="outputs/reference_ppt_files")
        self.excel_agent = ExcelAgent(output_folder="outputs/reference_excel_files")

    def handle(self, user_task):
        if not isinstance(user_task, str) or not user_task.strip():
            return "Reference Imitation Agent 没有收到有效任务。"

        file_path = self.file_reader_agent.extract_file_path(user_task)
        if not file_path:
            return "Reference Imitation Agent 没有找到参考文件路径，请提供 .docx、.pptx 或 .xlsx 文件路径。"

        if not file_path.exists():
            return f"Reference Imitation Agent 没有找到参考文件：{file_path}"

        if file_path.suffix.lower() not in [".docx", ".pptx", ".xlsx"]:
            return f"Reference Imitation Agent 暂只支持参考 Word、PPT、Excel 文件：{file_path.suffix}"

        try:
            reference_content = self.qa_agent.read_file_content(file_path)
        except OSError as error:
            return f"Reference Imitation Agent 读取参考文件失败：{error}"

        topic = self.extract_new_topic(user_task, file_path)
        if file_path.suffix.lower() == ".docx":
            output_path = self.create_word_like_file(topic, reference_content)
            file_type = "Word"
        elif file_path.suffix.lower() == ".pptx":
            output_path = self.create_ppt_like_file(topic, reference_content)
            file_type = "PPT"
        else:
            output_path = self.create_excel_like_file(topic, reference_content)
            file_type = "Excel"

        return (
            f"Reference Imitation Agent 已生成参考仿写 {file_type} 成品文件。\n"
            f"任务内容：{user_task.strip()}\n"
            f"参考文件位置：{file_path}\n"
            f"仿写主题：{topic}\n"
            f"文件位置：{output_path}"
        )

    def extract_new_topic(self, user_task, file_path):
        topic = user_task.replace(str(file_path), " ")
        removable_words = [
            "请",
            "帮我",
            "按照",
            "参考",
            "仿写",
            "模仿",
            "生成",
            "制作",
            "一份",
            "新的",
            "Word",
            "PPT",
            "Excel",
            "word",
            "ppt",
            "excel",
            "文档",
            "演示稿",
            "表格",
            "关于",
        ]
        for word in removable_words:
            topic = topic.replace(word, " ")

        cleaned_parts = [part for part in topic.replace("：", " ").replace(":", " ").split() if part]
        return " ".join(cleaned_parts).strip(" ，。；;") or "参考文件仿写成品"

    def create_word_like_file(self, topic, reference_content):
        headings = self.extract_reference_lines(reference_content, limit=6)
        paragraphs = [("title", topic)]
        paragraphs.append(("heading", "文档摘要"))
        paragraphs.append(("text", f"本文参考原文件的章节层级和表达节奏，围绕“{topic}”形成新的完整文档。"))

        if not headings:
            headings = ["背景与目标", "重点内容", "实施安排", "结论"]

        for index, heading in enumerate(headings, start=1):
            section_title = self.clean_section_title(heading, index)
            paragraphs.append(("heading", section_title))
            paragraphs.append(("text", self.build_word_section_content(topic, section_title, index)))

        output_path = self.word_agent.output_folder / self.word_agent.build_file_name()
        self.word_agent.output_folder.mkdir(parents=True, exist_ok=True)
        self.word_agent.write_docx(output_path, paragraphs)
        return output_path

    def create_ppt_like_file(self, topic, reference_content):
        titles = self.extract_reference_lines(reference_content, limit=5)
        if not titles:
            titles = ["背景", "核心内容", "执行计划", "结论"]

        slides = [
            {"title": topic, "bullets": [f"主题：{topic}", "目标：形成结构清晰、可直接汇报的演示稿"]},
            {"title": "目录", "bullets": [self.clean_section_title(title, index) for index, title in enumerate(titles, start=1)]},
        ]

        for index, title in enumerate(titles, start=1):
            section_title = self.clean_section_title(title, index)
            slides.append(
                {
                    "title": section_title,
                    "bullets": self.build_ppt_bullets(topic, section_title, index),
                }
            )

        output_path = self.ppt_agent.output_folder / self.ppt_agent.build_file_name()
        self.ppt_agent.output_folder.mkdir(parents=True, exist_ok=True)
        self.ppt_agent.write_pptx(output_path, slides)
        return output_path

    def create_excel_like_file(self, topic, reference_content):
        rows = [
            ["表格类型", "参考仿写表格"],
            ["表格主题", topic],
            [],
            ["序号", "模块", "内容", "状态", "备注"],
        ]

        reference_lines = self.extract_reference_lines(reference_content, limit=6)
        if not reference_lines:
            reference_lines = ["核心事项", "执行安排", "质量检查"]

        for index, line in enumerate(reference_lines, start=1):
            rows.append([str(index), self.clean_section_title(line, index), self.build_excel_content(topic, index), "进行中", "按成品任务推进"])

        rows = self.excel_agent.add_support_rows(rows)
        output_path = self.excel_agent.output_folder / self.excel_agent.build_file_name()
        self.excel_agent.output_folder.mkdir(parents=True, exist_ok=True)
        self.excel_agent.write_xlsx(output_path, rows)
        return output_path

    def extract_reference_lines(self, reference_content, limit):
        if not isinstance(reference_content, str):
            return []

        lines = []
        for raw_line in reference_content.splitlines():
            line = raw_line.strip().strip("-# ")
            if len(line) < 2:
                continue
            if line in lines:
                continue
            lines.append(line[:40])
            if len(lines) >= limit:
                break
        return lines

    def clean_section_title(self, raw_title, index):
        cleaned_title = raw_title.strip().strip("：:，。")
        if not cleaned_title:
            return f"第{index}部分"
        if len(cleaned_title) > 22:
            return cleaned_title[:22]
        return cleaned_title

    def build_word_section_content(self, topic, section_title, index):
        if index == 1:
            return f"本部分围绕“{topic}”说明基本背景和写作目的，延续参考文件先交代主题、再展开论述的方式，使读者能够快速理解文档要解决的问题。"
        if index == 2:
            return f"本部分结合“{section_title}”展开重点内容，强调事实、判断和行动之间的关系，避免停留在空泛描述上。"
        if index == 3:
            return f"本部分围绕执行安排展开，明确关键任务、参与对象和推进节奏，使“{topic}”能够从文字表达转化为具体行动。"
        return f"本部分对“{topic}”进行收束，突出主要结论和后续价值，使整份文档形成完整闭环。"

    def build_ppt_bullets(self, topic, section_title, index):
        if index == 1:
            return [f"说明“{topic}”的背景", "明确本页核心判断", "承接后续内容"]
        if index == 2:
            return [f"展开“{section_title}”的重点", "提炼主要信息", "突出可执行结论"]
        if index == 3:
            return ["明确行动安排", "说明责任和节奏", "形成推进路径"]
        return ["总结核心观点", "强调最终价值", "给出后续方向"]

    def build_excel_content(self, topic, index):
        content_map = {
            1: f"{topic}的基础信息整理",
            2: f"{topic}的重点事项推进",
            3: f"{topic}的质量检查记录",
        }
        return content_map.get(index, f"{topic}的配套内容")
