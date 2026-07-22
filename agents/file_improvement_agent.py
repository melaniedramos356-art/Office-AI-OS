from agents.creation_brief_agent import CreationBriefAgent
from agents.file_reader_agent import FileReaderAgent


class FileImprovementAgent:
    """已有 Office 文件的改进入口：生成任务单，不在本地重写成品。"""

    def __init__(self, creation_brief_agent=None, file_reader_agent=None):
        self.creation_brief_agent = creation_brief_agent or CreationBriefAgent()
        self.file_reader_agent = file_reader_agent or FileReaderAgent()

    def handle(self, user_task):
        if not isinstance(user_task, str) or not user_task.strip():
            return "文件改进任务单生成失败：需求不能为空。"

        file_path = self.file_reader_agent.extract_file_path(user_task)
        if not file_path:
            return "文件改进任务单生成失败：请提供要改进的 .docx、.pptx 或 .xlsx 文件路径。"

        office_type = self.detect_office_type(file_path)
        if not office_type or not file_path.exists():
            return "文件改进任务单生成失败：未找到可支持的参考文件。"

        return self.creation_brief_agent.handle(
            office_type,
            user_task,
            reference_path=file_path,
            task_mode="improve",
        )

    def detect_office_type(self, file_path):
        return {".docx": "word", ".pptx": "ppt", ".xlsx": "excel"}.get(file_path.suffix.lower())
