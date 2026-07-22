from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape
from zipfile import ZIP_DEFLATED, ZipFile

from agents.inspiration_library import InspirationLibrary
from agents.model_advice_utils import is_unusable_model_result, split_advice_lines
from agents.production_technique_library import ProductionTechniqueLibrary
from agents.technique_library import TechniqueLibrary
from models.model_router import ModelRouter


class WordAgent:
    def __init__(self, output_folder="outputs/word_documents"):
        self.output_folder = Path(output_folder)
        self.inspiration_library = InspirationLibrary()
        self.production_technique_library = ProductionTechniqueLibrary()
        self.technique_library = TechniqueLibrary()
        self.model_router = ModelRouter()

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
            ("title", self.build_document_title(user_task, document_type)),
            ("heading", "原始需求"),
            ("text", user_task),
            ("heading", "文档类型"),
            ("text", document_type),
            ("heading", "文档摘要"),
            ("text", self.build_document_summary(user_task, document_type)),
        ]

        for title, content in sections:
            paragraphs.append(("heading", title))
            paragraphs.append(("text", content))

        paragraphs.extend(
            [
                ("heading", "AI 结构建议"),
                *[("bullet", advice) for advice in self.build_model_advice(user_task, document_type, sections)],
                ("heading", "通用制作技巧"),
                *[("bullet", technique) for technique in self.production_technique_library.get_techniques("word")],
                ("heading", "灵感素材查找建议"),
                *[("bullet", advice) for advice in self.build_inspiration_advice(user_task)],
                ("heading", "素材库生成建议"),
                *[("bullet", advice) for advice in self.technique_library.get_advice("word")],
                ("heading", "待确认事项"),
                ("bullet", "请补充具体数据、时间、人员或业务背景。"),
                ("bullet", "请检查是否需要继续完善为正式可交付版本。"),
            ]
        )

        return paragraphs

    def build_document_title(self, user_task, document_type):
        if document_type == "大学生暑假安全教育班会文案":
            return "大学生暑假安全宣传教育主题班会文案"

        return "办公文档草稿"

    def build_document_summary(self, user_task, document_type):
        if document_type == "大学生暑假安全教育班会文案":
            return (
                "这是一份面向大学生的暑假安全宣传教育主题班会文案，"
                "重点围绕防溺水、交通安全、网络安全、兼职实习安全、心理健康和应急联系展开，"
                "可直接用于班会主持、班级通知或安全教育材料。"
            )

        return (
            f"这是一份{document_type}草稿，核心需求是：{user_task}。"
            "当前版本先搭建基础结构，后续需要补充真实数据、案例和责任信息。"
        )

    def build_model_advice(self, user_task, document_type, sections):
        section_titles = "、".join([section[0] for section in sections])
        prompt = (
            "请为下面的 Word 办公文档生成 3 条结构优化建议。"
            "要求：只输出 3 行，每行一条建议，不要输出长篇解释。\n\n"
            f"文档类型：{document_type}\n"
            f"用户需求：{user_task}\n"
            f"当前章节：{section_titles}"
        )
        generation = self.model_router.generate("word", prompt)
        route_info = generation.get("route", {})
        result = generation.get("result", "")

        if route_info.get("status") != "available" or is_unusable_model_result(result):
            return self.build_fallback_model_advice()

        return split_advice_lines(result, self.build_fallback_model_advice())

    def build_fallback_model_advice(self):
        return [
            "先写结论和目的，再补充背景和过程。",
            "每个章节只处理一个主题，避免把问题、原因和计划混在一起。",
            "关键结论后面预留数据、案例或截图位置，方便后续补强可信度。",
        ]

    def build_inspiration_advice(self, user_task):
        source_lines = self.inspiration_library.build_source_lines(user_task, limit=5)
        keyword_lines = self.inspiration_library.build_search_keywords(user_task)[:3]
        advice = []

        for source_line in source_lines:
            advice.append(source_line.replace("- ", "", 1))

        for keyword in keyword_lines:
            advice.append(f"搜索词：{keyword}")

        return advice

    def detect_document_type(self, user_task):
        if self.is_student_summer_safety_task(user_task):
            return "大学生暑假安全教育班会文案"

        if "通知" in user_task:
            return "通知"

        if "合同" in user_task or "协议" in user_task:
            return "合同/协议草稿"

        if "报告" in user_task or "总结" in user_task or "汇报" in user_task:
            return "报告/总结"

        if "文章" in user_task:
            return "文章"

        return "通用文档"

    def is_student_summer_safety_task(self, user_task):
        required_keywords = ["安全"]
        student_keywords = ["大学生", "学生", "班会"]
        summer_keywords = ["暑假", "假期", "暑期"]

        has_required = all(keyword in user_task for keyword in required_keywords)
        has_student = any(keyword in user_task for keyword in student_keywords)
        has_summer = any(keyword in user_task for keyword in summer_keywords)
        return has_required and has_student and has_summer

    def build_sections(self, document_type):
        if document_type == "大学生暑假安全教育班会文案":
            return [
                (
                    "一、班会主题",
                    "安全度暑假，平安再相聚。引导同学们增强安全意识，提前识别假期常见风险，做到离校不离安全、放假不放松防范。",
                ),
                (
                    "二、班会目标",
                    "通过本次班会，使同学们了解暑假期间容易出现的溺水、交通、网络诈骗、兼职实习、消防用电、心理健康等风险，掌握基本防范方法，明确遇到紧急情况时的求助渠道。",
                ),
                (
                    "三、开场主持词",
                    "同学们，暑假即将开始，假期是放松身心、提升自我的时间，但安全永远是第一位的。今天我们围绕暑假安全开展主题班会，希望大家把安全提醒真正记在心里、落实到行动中，平安离校，平安返校。",
                ),
                (
                    "四、重点安全提醒",
                    "第一，防溺水安全：不私自下水游泳，不到无安全设施、无救援人员的水域玩耍。第二，交通安全：外出遵守交通规则，不乘坐无牌、超载或存在安全隐患的车辆。第三，网络安全：警惕刷单返利、冒充客服、虚假中奖、游戏交易等诈骗信息，不随意转账，不泄露验证码。第四，兼职实习安全：选择正规平台和单位，不轻信高薪兼职，不提前缴纳押金、培训费或保证金。第五，消防和用电安全：离开宿舍或家中时关闭电源，不私拉乱接电线，不使用违规电器。",
                ),
                (
                    "五、互动提问",
                    "问题一：如果收到陌生人发来的兼职链接并要求先交押金，应该怎么做？问题二：同伴邀请去野外水域游泳时，应该如何劝阻？问题三：假期外出前，应该把行程告诉谁？通过提问让同学们把安全知识转化成具体判断。",
                ),
                (
                    "六、假期行动倡议",
                    "请同学们做到三主动：主动向家人说明假期安排，主动远离危险场所，主动保存辅导员、班主任、家人和紧急求助电话。做到三不做：不参与高风险活动，不轻信陌生信息，不隐瞒突发情况。",
                ),
                (
                    "七、结束语",
                    "安全不是一句口号，而是每一次选择。希望大家在暑假期间合理安排学习、生活和社会实践，保持联系畅通，遇到困难及时求助。祝全体同学度过一个平安、充实、健康的暑假。",
                ),
                (
                    "八、班会记录建议",
                    "可记录参会人数、主持人、班会时间、重点提醒内容、互动问题回答情况和学生安全承诺情况，便于后续留档。",
                ),
            ]

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
