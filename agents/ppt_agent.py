from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape
from zipfile import ZIP_DEFLATED, ZipFile

from agents.inspiration_library import InspirationLibrary
from agents.production_technique_library import ProductionTechniqueLibrary
from agents.technique_library import TechniqueLibrary
from models.model_router import ModelRouter


class PPTAgent:
    def __init__(self, output_folder="outputs/ppt_files"):
        self.output_folder = Path(output_folder)
        self.inspiration_library = InspirationLibrary()
        self.production_technique_library = ProductionTechniqueLibrary()
        self.technique_library = TechniqueLibrary()
        self.model_router = ModelRouter()

    def handle(self, user_task):
        if not isinstance(user_task, str) or not user_task.strip():
            return "PPT Agent 没有收到有效任务。"

        cleaned_task = user_task.strip()

        try:
            presentation_path = self.create_presentation(cleaned_task)
        except OSError as error:
            return f"PPT Agent 创建 PPT 文件失败：{error}"

        return (
            "PPT Agent 已生成 PPT 文件。\n"
            f"任务内容：{cleaned_task}\n"
            f"文件位置：{presentation_path}"
        )

    def create_presentation(self, user_task):
        self.output_folder.mkdir(parents=True, exist_ok=True)

        file_name = self.build_file_name()
        presentation_path = self.output_folder / file_name
        slides = self.build_slide_data(user_task)

        self.write_pptx(presentation_path, slides)
        return presentation_path

    def build_file_name(self):
        time_text = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        return f"ppt_file_{time_text}.pptx"

    def build_slide_data(self, user_task):
        presentation_type = self.detect_presentation_type(user_task)
        slides = self.build_slides(presentation_type)
        agenda_slide = self.build_agenda_slide(slides)

        slide_data = [
            {
                "title": f"{presentation_type}",
                "bullets": [user_task, "自动生成的演示稿草稿", "后续可继续补充真实数据和图片"],
            }
        ] + [agenda_slide] + slides

        slide_data.append(
            {
                "title": "AI 结构建议",
                "bullets": self.build_model_advice(user_task, presentation_type, slides),
            }
        )

        slide_data.append(
            {
                "title": "通用制作技巧",
                "bullets": self.production_technique_library.get_techniques("ppt"),
            }
        )

        slide_data.append(
            {
                "title": "灵感素材查找建议",
                "bullets": self.build_inspiration_advice(user_task),
            }
        )

        slide_data.append(
            {
                "title": "素材库生成建议",
                "bullets": self.technique_library.get_advice("ppt"),
            }
        )
        return slide_data

    def build_agenda_slide(self, slides):
        agenda_items = []
        for slide in slides:
            title = slide.get("title", "").strip()
            if title:
                agenda_items.append(title)

        return {
            "title": "目录",
            "bullets": agenda_items[:5] or ["背景", "核心内容", "结论", "下一步"],
        }

    def build_model_advice(self, user_task, presentation_type, slides):
        slide_titles = "、".join([slide["title"] for slide in slides])
        prompt = (
            "请为下面的 PPT 生成 3 条结构优化建议。"
            "要求：只输出 3 行，每行一条建议，不要输出长篇解释。\n\n"
            f"PPT 类型：{presentation_type}\n"
            f"用户需求：{user_task}\n"
            f"当前页面：{slide_titles}"
        )
        generation = self.model_router.generate("ppt", prompt)
        route_info = generation.get("route", {})
        result = generation.get("result", "")

        if route_info.get("status") != "available" or self.is_unusable_model_result(result):
            return self.build_fallback_model_advice()

        return self.split_model_advice(result)

    def build_fallback_model_advice(self):
        return [
            "先讲结论，再展开背景和依据。",
            "每页只保留 3 个以内重点，避免一页塞太多文字。",
            "关键页预留图片、图表或案例位置，方便后续增强视觉效果。",
        ]

    def is_unusable_model_result(self, result):
        if not isinstance(result, str) or not result.strip():
            return True

        error_keywords = ["调用失败", "未设置", "返回格式异常", "没有收到有效提示词", "Mock"]
        for keyword in error_keywords:
            if keyword in result:
                return True
        return False

    def split_model_advice(self, result):
        advice_items = []
        for line in result.splitlines():
            cleaned_line = line.strip().lstrip("-").lstrip("1234567890.、 ").strip()
            if cleaned_line:
                advice_items.append(cleaned_line)

        return advice_items[:3] or self.build_fallback_model_advice()

    def build_inspiration_advice(self, user_task):
        source_lines = self.inspiration_library.build_source_lines(user_task, limit=5)
        keyword_lines = self.inspiration_library.build_search_keywords(user_task)[:3]
        advice = []

        for source_line in source_lines:
            advice.append(source_line)

        for keyword in keyword_lines:
            advice.append(f"搜索词：{keyword}")

        return advice

    def detect_presentation_type(self, user_task):
        if "销售" in user_task or "营收" in user_task or "收入" in user_task:
            return "销售汇报"

        if "项目" in user_task or "进度" in user_task or "阶段" in user_task:
            return "项目汇报"

        if "培训" in user_task or "课程" in user_task:
            return "培训课件"

        if "产品" in user_task or "方案" in user_task:
            return "产品/方案介绍"

        return "通用演示稿"

    def build_slides(self, presentation_type):
        if presentation_type == "销售汇报":
            return [
                {"title": "销售概览", "bullets": ["总销售额", "目标完成率", "关键变化"]},
                {"title": "重点数据", "bullets": ["按产品、区域或客户拆分", "列出主要增长点"]},
                {"title": "问题与原因", "bullets": ["未达预期的部分", "可能原因"]},
                {"title": "下一步计划", "bullets": ["重点行动", "负责人", "时间节点"]},
            ]

        if presentation_type == "项目汇报":
            return [
                {"title": "项目背景", "bullets": ["项目目标", "当前阶段"]},
                {"title": "已完成内容", "bullets": ["关键成果", "已交付事项"]},
                {"title": "风险与问题", "bullets": ["当前问题", "影响范围", "解决建议"]},
                {"title": "下一步计划", "bullets": ["后续任务", "负责人", "截止时间"]},
            ]

        if presentation_type == "培训课件":
            return [
                {"title": "学习目标", "bullets": ["学完后能掌握什么"]},
                {"title": "核心知识", "bullets": ["重点概念", "操作步骤"]},
                {"title": "案例练习", "bullets": ["示例场景", "练习任务"]},
                {"title": "总结与作业", "bullets": ["本节重点", "后续练习"]},
            ]

        if presentation_type == "产品/方案介绍":
            return [
                {"title": "用户痛点", "bullets": ["当前问题", "影响结果"]},
                {"title": "解决方案", "bullets": ["核心能力", "使用流程"]},
                {"title": "优势与案例", "bullets": ["主要优势", "示例效果"]},
                {"title": "推进计划", "bullets": ["下一步动作", "需要支持"]},
            ]

        return [
            {"title": "背景", "bullets": ["为什么做这件事", "当前情况"]},
            {"title": "核心内容", "bullets": ["重点一", "重点二", "重点三"]},
            {"title": "结论", "bullets": ["主要结论", "判断依据"]},
            {"title": "下一步", "bullets": ["行动计划", "时间安排"]},
        ]

    def write_pptx(self, presentation_path, slides):
        with ZipFile(presentation_path, "w", ZIP_DEFLATED) as pptx_file:
            pptx_file.writestr("[Content_Types].xml", self.build_content_types_xml(len(slides)))
            pptx_file.writestr("_rels/.rels", self.build_root_relationships_xml())
            pptx_file.writestr("ppt/presentation.xml", self.build_presentation_xml(len(slides)))
            pptx_file.writestr("ppt/_rels/presentation.xml.rels", self.build_presentation_relationships_xml(len(slides)))
            pptx_file.writestr("ppt/presProps.xml", self.build_empty_xml("p:presentationPr"))
            pptx_file.writestr("ppt/viewProps.xml", self.build_empty_xml("p:viewPr"))
            pptx_file.writestr("ppt/tableStyles.xml", self.build_table_styles_xml())

            for index, slide in enumerate(slides, start=1):
                pptx_file.writestr(f"ppt/slides/slide{index}.xml", self.build_slide_xml(slide))

    def build_content_types_xml(self, slide_count):
        slide_overrides = "".join(
            [
                f'<Override PartName="/ppt/slides/slide{index}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
                for index in range(1, slide_count + 1)
            ]
        )
        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>'
            '<Override PartName="/ppt/presProps.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presProps+xml"/>'
            '<Override PartName="/ppt/viewProps.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.viewProps+xml"/>'
            '<Override PartName="/ppt/tableStyles.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.tableStyles+xml"/>'
            f"{slide_overrides}"
            "</Types>"
        )

    def build_root_relationships_xml(self):
        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>'
            "</Relationships>"
        )

    def build_presentation_xml(self, slide_count):
        slide_ids = "".join(
            [
                f'<p:sldId id="{255 + index}" r:id="rId{index}"/>'
                for index in range(1, slide_count + 1)
            ]
        )
        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
            'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
            f"<p:sldIdLst>{slide_ids}</p:sldIdLst>"
            '<p:sldSz cx="12192000" cy="6858000" type="wide"/>'
            '<p:notesSz cx="6858000" cy="9144000"/>'
            "</p:presentation>"
        )

    def build_presentation_relationships_xml(self, slide_count):
        slide_relationships = "".join(
            [
                f'<Relationship Id="rId{index}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{index}.xml"/>'
                for index in range(1, slide_count + 1)
            ]
        )
        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            f"{slide_relationships}"
            "</Relationships>"
        )

    def build_slide_xml(self, slide):
        title_shape = self.build_text_shape_xml(2, slide["title"], 700000, 450000, 10800000, 900000, 40, True)
        bullet_shapes = []
        for index, bullet in enumerate(slide["bullets"], start=1):
            bullet_shapes.append(
                self.build_text_shape_xml(
                    2 + index,
                    f"• {bullet}",
                    950000,
                    1550000 + (index - 1) * 720000,
                    10200000,
                    560000,
                    24,
                    False,
                )
            )

        shapes_xml = title_shape + "".join(bullet_shapes)
        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
            'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
            "<p:cSld>"
            "<p:spTree>"
            "<p:nvGrpSpPr><p:cNvPr id=\"1\" name=\"\"/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>"
            "<p:grpSpPr><a:xfrm><a:off x=\"0\" y=\"0\"/><a:ext cx=\"0\" cy=\"0\"/><a:chOff x=\"0\" y=\"0\"/><a:chExt cx=\"0\" cy=\"0\"/></a:xfrm></p:grpSpPr>"
            f"{shapes_xml}"
            "</p:spTree>"
            "</p:cSld>"
            "<p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>"
            "</p:sld>"
        )

    def build_text_shape_xml(self, shape_id, text, x, y, width, height, font_size, is_bold):
        safe_text = escape(text)
        bold_xml = ' b="1"' if is_bold else ""
        return (
            "<p:sp>"
            f'<p:nvSpPr><p:cNvPr id="{shape_id}" name="TextBox {shape_id}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{width}" cy="{height}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr>'
            "<p:txBody><a:bodyPr wrap=\"square\"/><a:lstStyle/>"
            f'<a:p><a:r><a:rPr lang="zh-CN" sz="{font_size * 100}"{bold_xml}/><a:t>{safe_text}</a:t></a:r></a:p>'
            "</p:txBody>"
            "</p:sp>"
        )

    def build_empty_xml(self, root_name):
        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            f'<{root_name} xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
            f'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
            f'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"/>'
        )

    def build_table_styles_xml(self):
        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<a:tblStyleLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" def="{5940675A-B579-460E-94D1-54222C63F5DA}"/>'
        )
