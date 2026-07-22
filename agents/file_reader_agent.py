from pathlib import Path

from agents.qa_agent import QAAgent


class FileReaderAgent:
    def __init__(self):
        self.qa_agent = QAAgent()
        self.supported_suffixes = [".docx", ".xlsx", ".pptx", ".md", ".txt", ".csv"]

    def handle(self, user_task):
        if not isinstance(user_task, str) or not user_task.strip():
            return "File Reader Agent 没有收到有效任务。"

        file_path = self.extract_file_path(user_task)
        if not file_path:
            return "File Reader Agent 没有找到文件路径，请在任务里提供 .docx、.pptx、.xlsx、.md、.txt 或 .csv 文件路径。"

        return self.inspect_file(file_path, user_task.strip())

    def extract_file_path(self, user_task):
        for raw_part in user_task.replace('"', " ").replace("'", " ").split():
            cleaned_part = raw_part.strip().strip("，。；;")
            path = Path(cleaned_part)
            if path.suffix.lower() in self.supported_suffixes:
                return path
        return None

    def inspect_file(self, file_path, user_task):
        if file_path.suffix.lower() not in self.supported_suffixes:
            return f"File Reader Agent 暂不支持这种文件类型：{file_path.suffix}"

        if not file_path.exists():
            return f"File Reader Agent 没有找到文件：{file_path}"

        if not file_path.is_file():
            return f"File Reader Agent 收到的不是文件：{file_path}"

        try:
            file_content = self.qa_agent.read_file_content(file_path)
        except OSError as error:
            return f"File Reader Agent 读取文件失败：{error}"

        preview = self.build_preview(file_content)
        advice = self.build_next_step_advice(file_path)

        return (
            "File Reader Agent 已读取文件。\n"
            f"任务内容：{user_task}\n"
            f"文件位置：{file_path}\n"
            f"文件类型：{file_path.suffix.lower()}\n"
            f"字符数量：{len(file_content)}\n\n"
            "## 内容预览\n"
            f"{preview}\n\n"
            "## 下一步建议\n"
            f"{advice}"
        )

    def build_preview(self, file_content):
        if not isinstance(file_content, str) or not file_content.strip():
            return "文件内容为空，建议先检查文件是否损坏。"

        lines = [line.strip() for line in file_content.splitlines() if line.strip()]
        preview_lines = lines[:12]
        preview = "\n".join([f"- {line[:120]}" for line in preview_lines])

        if len(lines) > len(preview_lines):
            preview += f"\n- 其余 {len(lines) - len(preview_lines)} 行已省略。"

        return preview

    def build_next_step_advice(self, file_path):
        suffix = file_path.suffix.lower()

        if suffix == ".docx":
            return "建议下一步交给 Word Agent 做结构优化、文案润色和语言丰富。"

        if suffix == ".pptx":
            return "建议下一步交给 PPT Agent 做页面结构、版面设计和图片素材建议。"

        if suffix == ".xlsx":
            return "建议下一步交给 Excel Agent 做字段检查、数据规则、图表建议和分析看板规划。"

        return "建议下一步交给 AI Butler Agent 判断应由哪个办公 Agent 继续处理。"
