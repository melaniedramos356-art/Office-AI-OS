from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape
from zipfile import ZIP_DEFLATED, ZipFile


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
        paragraphs = self.build_document_paragraphs(user_task)

        self.write_docx(document_path, paragraphs)
        return document_path

    def build_file_name(self):
        time_text = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        return f"word_document_{time_text}.docx"

    def build_document_paragraphs(self, user_task):
        document_type = self.detect_document_type(user_task)
        sections = self.build_sections(document_type)

        paragraphs = [
            ("title", "办公文档草稿"),
            ("heading", "原始需求"),
            ("text", user_task),
            ("heading", "文档类型"),
            ("text", document_type),
        ]

        for title, content in sections:
            paragraphs.append(("heading", title))
            paragraphs.append(("text", content))

        paragraphs.extend(
            [
                ("heading", "待确认事项"),
                ("bullet", "请补充具体数据、时间、人员或业务背景。"),
                ("bullet", "请检查是否需要继续完善为正式可交付版本。"),
            ]
        )

        return paragraphs

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
                ("通知事项", "请在这里填写需要通知的具体事情。"),
                ("时间安排", "请在这里填写开始时间、结束时间和关键节点。"),
                ("注意事项", "请在这里填写参与人员需要注意的内容。"),
            ]

        if document_type == "合同/协议草稿":
            return [
                ("合作事项", "请在这里填写双方要合作或约定的具体事项。"),
                ("双方责任", "请在这里填写甲方、乙方分别需要完成的事情。"),
                ("待确认条款", "请在这里填写金额、时间、交付物、违约处理等内容。"),
            ]

        if document_type == "报告/总结":
            return [
                ("背景", "请在这里填写这份报告或总结的背景。"),
                ("重点内容", "请在这里填写主要成果、问题和数据。"),
                ("下一步计划", "请在这里填写后续行动安排。"),
            ]

        if document_type == "文章":
            return [
                ("标题方向", "请在这里填写文章标题或主题。"),
                ("正文草稿", "请在这里展开正文内容。"),
                ("结尾", "请在这里填写总结或行动建议。"),
            ]

        return [
            ("主题", "请在这里填写文档主题。"),
            ("正文", "请在这里填写主要内容。"),
            ("补充说明", "请在这里填写需要补充的信息。"),
        ]

    def write_docx(self, document_path, paragraphs):
        document_xml = self.build_document_xml(paragraphs)

        with ZipFile(document_path, "w", ZIP_DEFLATED) as docx_file:
            docx_file.writestr("[Content_Types].xml", self.build_content_types_xml())
            docx_file.writestr("_rels/.rels", self.build_relationships_xml())
            docx_file.writestr("word/document.xml", document_xml)

    def build_document_xml(self, paragraphs):
        paragraph_xml = "\n".join([self.build_paragraph_xml(style, text) for style, text in paragraphs])
        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            "<w:body>"
            f"{paragraph_xml}"
            '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/></w:sectPr>'
            "</w:body>"
            "</w:document>"
        )

    def build_paragraph_xml(self, style, text):
        safe_text = escape(text)
        properties = self.build_paragraph_properties(style)
        return f"<w:p>{properties}<w:r>{self.build_run_properties(style)}<w:t>{safe_text}</w:t></w:r></w:p>"

    def build_paragraph_properties(self, style):
        if style == "title":
            return '<w:pPr><w:jc w:val="center"/></w:pPr>'

        if style == "bullet":
            return '<w:pPr><w:ind w:left="720"/></w:pPr>'

        return ""

    def build_run_properties(self, style):
        if style == "title":
            return '<w:rPr><w:b/><w:sz w:val="32"/></w:rPr>'

        if style == "heading":
            return '<w:rPr><w:b/><w:sz w:val="26"/></w:rPr>'

        return '<w:rPr><w:sz w:val="22"/></w:rPr>'

    def build_content_types_xml(self):
        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
            "</Types>"
        )

    def build_relationships_xml(self):
        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
            "</Relationships>"
        )
