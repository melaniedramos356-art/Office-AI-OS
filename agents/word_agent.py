from datetime import datetime
from pathlib import Path


class WordAgent:
    def __init__(self, output_folder="outputs/word_documents"):
        self.output_folder = Path(output_folder)

    def handle(self, user_task):
        if not isinstance(user_task, str) or not user_task.strip():
            return "Word Agent 没有收到有效任务。"

        cleaned_task = user_task.strip()

        try:
            document_path = self.create_document(cleaned_task)
        except OSError as error:
            return f"Word Agent 创建文档失败：{error}"

        return (
            "Word Agent 已生成文档。\n"
            f"任务内容：{cleaned_task}\n"
            f"文件位置：{document_path}"
        )

    def create_document(self, user_task):
        self.output_folder.mkdir(parents=True, exist_ok=True)

        file_name = self.build_file_name()
        document_path = self.output_folder / file_name
        document_content = self.build_document_content(user_task)

        document_path.write_text(document_content, encoding="utf-8")
        return document_path

    def build_file_name(self):
        time_text = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        return f"word_document_{time_text}.md"

    def build_document_content(self, user_task):
        document_type = self.detect_document_type(user_task)
        sections = self.build_sections(document_type)

        section_text = "\n\n".join(sections)
        return (
            "# 办公文档草稿\n\n"
            f"## 原始需求\n\n{user_task}\n\n"
            f"## 文档类型\n\n{document_type}\n\n"
            f"{section_text}\n\n"
            "## 待确认事项\n\n"
            "- 请补充具体数据、时间、人员或业务背景。\n"
            "- 请检查是否需要改成正式 Word、PDF 或 PPT 格式。\n"
        )

    def detect_document_type(self, user_task):
        if "通知" in user_task:
            return "通知"

        if "合同" in user_task or "协议" in user_task:
            return "合同/协议草稿"

        if "报告" in user_task or "总结" in user_task or "汇报" in user_task:
            return "报告/总结"

        if "文章" in user_task:
            return "文章"

        return "通用文档"

    def build_sections(self, document_type):
        if document_type == "通知":
            return [
                "## 通知事项\n\n请在这里填写需要通知的具体事情。",
                "## 时间安排\n\n请在这里填写开始时间、结束时间和关键节点。",
                "## 注意事项\n\n请在这里填写参与人员需要注意的内容。",
            ]

        if document_type == "合同/协议草稿":
            return [
                "## 合作事项\n\n请在这里填写双方要合作或约定的具体事项。",
                "## 双方责任\n\n请在这里填写甲方、乙方分别需要完成的事情。",
                "## 待确认条款\n\n请在这里填写金额、时间、交付物、违约处理等内容。",
            ]

        if document_type == "报告/总结":
            return [
                "## 背景\n\n请在这里填写这份报告或总结的背景。",
                "## 重点内容\n\n请在这里填写主要成果、问题和数据。",
                "## 下一步计划\n\n请在这里填写后续行动安排。",
            ]

        if document_type == "文章":
            return [
                "## 标题方向\n\n请在这里填写文章标题或主题。",
                "## 正文草稿\n\n请在这里展开正文内容。",
                "## 结尾\n\n请在这里填写总结或行动建议。",
            ]

        return [
            "## 主题\n\n请在这里填写文档主题。",
            "## 正文\n\n请在这里填写主要内容。",
            "## 补充说明\n\n请在这里填写需要补充的信息。",
        ]
