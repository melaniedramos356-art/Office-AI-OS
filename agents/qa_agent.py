from pathlib import Path
import re
from xml.etree import ElementTree
from zipfile import BadZipFile, ZipFile


class QAAgent:
    def check_task_result(self, task_result, original_task):
        if not isinstance(task_result, str) or not task_result.strip():
            return "QA Agent 质量检查结果：未通过，任务结果为空。"

        file_path = self.extract_file_path(task_result)
        if not file_path:
            return "QA Agent 质量检查结果：跳过，未发现可检查的文件位置。"

        return self.check_file(file_path, original_task)

    def extract_file_path(self, task_result):
        for line in task_result.splitlines():
            if line.startswith("文件位置："):
                raw_path = line.replace("文件位置：", "", 1).strip()
                if raw_path:
                    return Path(raw_path)
        return None

    def check_file(self, file_path, original_task):
        problems = []

        if not file_path.exists():
            return f"QA Agent 质量检查结果：未通过，文件不存在。文件位置：{file_path}"

        if not file_path.is_file():
            return f"QA Agent 质量检查结果：未通过，路径不是文件。文件位置：{file_path}"

        try:
            file_content = self.read_file_content(file_path)
        except OSError as error:
            return f"QA Agent 质量检查结果：未通过，文件读取失败：{error}"

        if not file_content.strip():
            problems.append("文件内容为空")

        if not self.is_relevant_to_task(file_content, original_task):
            problems.append("文件内容没有覆盖需求关键词")

        if file_path.suffix.lower() not in [".md", ".csv", ".txt", ".docx", ".xlsx", ".pptx"]:
            problems.append("文件类型暂未纳入当前检查范围")

        if problems:
            problem_text = "；".join(problems)
            return f"QA Agent 质量检查结果：未通过，{problem_text}。文件位置：{file_path}"

        return f"QA Agent 质量检查结果：通过。文件位置：{file_path}"

    def is_relevant_to_task(self, file_content, original_task):
        if not isinstance(original_task, str) or not original_task.strip():
            return True

        task_text = original_task.strip()
        if task_text in file_content:
            return True

        keywords = self.extract_task_keywords(task_text)
        if not keywords:
            return True

        matched_count = 0
        for keyword in keywords:
            if keyword in file_content:
                matched_count += 1

        required_count = min(2, max(1, len(keywords) // 3))
        return matched_count >= required_count

    def extract_task_keywords(self, task_text):
        cleaned_text = task_text
        stop_words = [
            "帮我",
            "生成",
            "做一份",
            "写一份",
            "制作",
            "新建",
            "关于",
            "大概",
            "左右",
            "给",
            "看",
            "一个",
            "一份",
            "文件",
            "文档",
            "表格",
            "演示稿",
            "ppt",
            "PPT",
            "word",
            "Word",
            "excel",
            "Excel",
            "页",
        ]

        for word in stop_words:
            cleaned_text = cleaned_text.replace(word, " ")

        raw_parts = re.split(r"[\s,，。；;：:\-_、/\\]+", cleaned_text)
        keywords = []
        for part in raw_parts:
            cleaned_part = part.strip()
            if len(cleaned_part) >= 2 and not cleaned_part.isdigit():
                keywords.extend(self.build_chinese_key_fragments(cleaned_part))
                keywords.append(cleaned_part)

        return self.unique_texts(keywords)[:24]

    def build_chinese_key_fragments(self, text):
        if not re.fullmatch(r"[\u4e00-\u9fff]+", text) or len(text) < 4:
            return []

        fragments = []
        for size in [3, 2, 4]:
            for index in range(0, len(text) - size + 1):
                fragments.append(text[index : index + size])

        return fragments

    def unique_texts(self, texts):
        unique_results = []
        seen_texts = set()
        for text in texts:
            key = text.lower()
            if key in seen_texts:
                continue
            seen_texts.add(key)
            unique_results.append(text)
        return unique_results

    def read_file_content(self, file_path):
        if file_path.suffix.lower() == ".csv":
            return file_path.read_text(encoding="utf-8-sig")

        if file_path.suffix.lower() == ".docx":
            return self.read_docx_content(file_path)

        if file_path.suffix.lower() == ".xlsx":
            return self.read_xlsx_content(file_path)

        if file_path.suffix.lower() == ".pptx":
            return self.read_pptx_content(file_path)

        return file_path.read_text(encoding="utf-8")

    def read_docx_content(self, file_path):
        try:
            with ZipFile(file_path, "r") as docx_file:
                document_xml = docx_file.read("word/document.xml")
        except (BadZipFile, KeyError) as error:
            raise OSError(f"无法读取 docx 内容：{error}")

        root = ElementTree.fromstring(document_xml)
        namespace = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
        texts = []

        for text_node in root.findall(".//w:t", namespace):
            if text_node.text:
                texts.append(text_node.text)

        return "\n".join(texts)

    def read_xlsx_content(self, file_path):
        try:
            with ZipFile(file_path, "r") as xlsx_file:
                worksheet_names = [
                    name
                    for name in xlsx_file.namelist()
                    if name.startswith("xl/worksheets/") and name.endswith(".xml")
                ]
                worksheet_xml_list = [xlsx_file.read(name) for name in worksheet_names]
        except (BadZipFile, KeyError) as error:
            raise OSError(f"无法读取 xlsx 内容：{error}")

        texts = []
        namespace = {"x": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}

        for worksheet_xml in worksheet_xml_list:
            root = ElementTree.fromstring(worksheet_xml)
            for text_node in root.findall(".//x:t", namespace):
                if text_node.text:
                    texts.append(text_node.text)

        return "\n".join(texts)

    def read_pptx_content(self, file_path):
        try:
            with ZipFile(file_path, "r") as pptx_file:
                slide_names = [
                    name
                    for name in pptx_file.namelist()
                    if name.startswith("ppt/slides/slide") and name.endswith(".xml")
                ]
                slide_xml_list = [pptx_file.read(name) for name in sorted(slide_names)]
        except (BadZipFile, KeyError) as error:
            raise OSError(f"无法读取 pptx 内容：{error}")

        texts = []
        namespace = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}

        for slide_xml in slide_xml_list:
            root = ElementTree.fromstring(slide_xml)
            for text_node in root.findall(".//a:t", namespace):
                if text_node.text:
                    texts.append(text_node.text)

        return "\n".join(texts)
