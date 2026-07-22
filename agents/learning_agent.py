import csv
from datetime import datetime
from pathlib import Path


class LearningAgent:
    def __init__(self, materials_folder="materials", memory_folder="memory"):
        self.materials_folder = Path(materials_folder)
        self.memory_folder = Path(memory_folder)
        self.supported_suffixes = [".md", ".txt", ".csv"]

    def handle(self, user_task):
        if not isinstance(user_task, str) or not user_task.strip():
            return "Learning Agent 没有收到有效任务。"

        cleaned_task = user_task.strip()

        try:
            learned_path, index_path, production_path, material_count = self.learn_from_materials(cleaned_task)
        except OSError as error:
            return f"Learning Agent 学习素材失败：{error}"

        return (
            "Learning Agent 已完成素材学习。\n"
            f"任务内容：{cleaned_task}\n"
            f"素材数量：{material_count}\n"
            f"文件位置：{learned_path}\n"
            f"索引位置：{index_path}\n"
            f"制作技巧位置：{production_path}"
        )

    def learn_from_materials(self, user_task):
        self.materials_folder.mkdir(parents=True, exist_ok=True)
        self.memory_folder.mkdir(parents=True, exist_ok=True)

        materials = self.collect_materials()
        learned_content = self.build_learned_content(user_task, materials)
        index_content = self.build_index_content(user_task, materials)
        advice_content = self.build_generation_advice_content(user_task, materials)
        production_content = self.build_production_techniques_content(user_task, materials)

        learned_path = self.memory_folder / "learned_techniques.md"
        index_path = self.memory_folder / "material_index.md"
        advice_path = self.memory_folder / "generation_advice.md"
        production_path = self.memory_folder / "production_techniques.md"

        learned_path.write_text(learned_content, encoding="utf-8")
        index_path.write_text(index_content, encoding="utf-8")
        advice_path.write_text(advice_content, encoding="utf-8")
        production_path.write_text(production_content, encoding="utf-8")

        return learned_path, index_path, production_path, len(materials)

    def collect_materials(self):
        if not self.materials_folder.exists():
            return []

        material_files = []
        for file_path in self.materials_folder.rglob("*"):
            if not file_path.is_file():
                continue

            if file_path.suffix.lower() not in self.supported_suffixes:
                continue

            if file_path.name.lower() == "readme.md":
                continue

            material_files.append(file_path)

        return [self.analyze_material(file_path) for file_path in sorted(material_files)]

    def analyze_material(self, file_path):
        section_name = self.detect_section_name(file_path)
        content = self.read_material_content(file_path)
        lines = [line.strip() for line in content.splitlines() if line.strip()]

        return {
            "section": section_name,
            "path": file_path,
            "title": self.detect_title(file_path, lines),
            "headings": self.detect_headings(lines),
            "keywords": self.detect_keywords(content),
            "line_count": len(lines),
        }

    def detect_section_name(self, file_path):
        try:
            relative_path = file_path.relative_to(self.materials_folder)
        except ValueError:
            return "unknown"

        if not relative_path.parts:
            return "unknown"

        return relative_path.parts[0]

    def read_material_content(self, file_path):
        if file_path.suffix.lower() == ".csv":
            return self.read_csv_content(file_path)

        return file_path.read_text(encoding="utf-8")

    def read_csv_content(self, file_path):
        rows = []
        with file_path.open("r", newline="", encoding="utf-8-sig") as file:
            reader = csv.reader(file)
            for row in reader:
                rows.append(" ".join(row))
        return "\n".join(rows)

    def detect_title(self, file_path, lines):
        for line in lines:
            if line.startswith("#"):
                return line.replace("#", "").strip()

        if lines:
            return lines[0][:40]

        return file_path.stem

    def detect_headings(self, lines):
        headings = []
        for line in lines:
            if line.startswith("#"):
                headings.append(line.replace("#", "").strip())

        return headings[:8]

    def detect_keywords(self, content):
        keyword_candidates = [
            "标题",
            "背景",
            "目标",
            "结构",
            "数据",
            "结论",
            "案例",
            "步骤",
            "风险",
            "计划",
            "截图",
            "来源",
            "表格",
            "页面",
            "汇报",
        ]

        found_keywords = []
        for keyword in keyword_candidates:
            if keyword in content:
                found_keywords.append(keyword)

        return found_keywords[:8]

    def build_learned_content(self, user_task, materials):
        time_text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        section_blocks = self.build_section_blocks(materials)

        return (
            "# 优秀素材学习结果\n\n"
            f"## 原始需求\n\n{user_task}\n\n"
            f"## 更新时间\n\n{time_text}\n\n"
            f"## 素材总数\n\n{len(materials)}\n\n"
            f"{section_blocks}\n\n"
            "## 使用建议\n\n"
            "- Word Agent 生成文档时，优先参考标题、背景、结论等结构。\n"
            "- Excel Agent 生成表格时，优先参考字段、统计口径和备注方式。\n"
            "- PPT Agent 生成大纲时，优先参考页面顺序和汇报逻辑。\n"
            "- Research Agent 生成计划时，优先参考来源、关键词和资料记录表。\n"
            "- Browser Agent 生成计划时，优先参考步骤、截图、页面和异常处理方式。\n"
        )

    def build_section_blocks(self, materials):
        if not materials:
            return (
                "## 暂无可学习素材\n\n"
                "请把优秀 `.md`、`.txt` 或 `.csv` 文件放到 `materials/对应板块/examples/` 后重新运行。"
            )

        grouped_materials = {}
        for material in materials:
            grouped_materials.setdefault(material["section"], []).append(material)

        blocks = []
        for section_name, section_materials in sorted(grouped_materials.items()):
            blocks.append(self.build_single_section_block(section_name, section_materials))

        return "\n\n".join(blocks)

    def build_single_section_block(self, section_name, section_materials):
        titles = [material["title"] for material in section_materials]
        headings = []
        keywords = []

        for material in section_materials:
            headings.extend(material["headings"])
            keywords.extend(material["keywords"])

        title_text = "\n".join([f"- {title}" for title in titles[:10]])
        heading_text = "\n".join([f"- {heading}" for heading in self.unique_items(headings)[:10]])
        keyword_text = "、".join(self.unique_items(keywords)[:12]) or "暂无明显关键词"

        return (
            f"## {section_name} 板块学习结果\n\n"
            f"### 素材数量\n\n{len(section_materials)}\n\n"
            f"### 素材标题\n\n{title_text}\n\n"
            f"### 常见结构\n\n{heading_text or '- 暂无明显标题结构'}\n\n"
            f"### 常见技巧关键词\n\n{keyword_text}"
        )

    def build_index_content(self, user_task, materials):
        lines = [
            "# 优秀素材索引",
            "",
            "## 原始需求",
            "",
            user_task,
            "",
            "| 板块 | 标题 | 文件路径 | 行数 | 关键词 |",
            "| --- | --- | --- | --- | --- |",
        ]

        for material in materials:
            keywords = "、".join(material["keywords"]) or "暂无"
            lines.append(
                f"| {material['section']} | {material['title']} | {material['path']} | {material['line_count']} | {keywords} |"
            )

        if not materials:
            lines.append("| 暂无 | 暂无素材 | 请添加素材 | 0 | 暂无 |")

        return "\n".join(lines) + "\n"

    def build_generation_advice_content(self, user_task, materials):
        time_text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        material_sections = self.unique_items([material["section"] for material in materials])
        all_sections = self.unique_items(material_sections + ["word", "excel", "ppt", "research", "browser"])

        blocks = []
        for section_name in all_sections:
            blocks.append(self.build_generation_advice_block(section_name, materials))

        return (
            "# 生成建议与图片搜索计划\n\n"
            f"## 原始需求\n\n{user_task}\n\n"
            f"## 更新时间\n\n{time_text}\n\n"
            "## 使用方式\n\n"
            "- 生成前先读取对应板块建议。\n"
            "- 素材库为空时使用内置建议；素材库有内容时叠加学习结果。\n"
            "- 图片只先生成搜索关键词和使用建议，不自动下载，避免版权和来源风险。\n\n"
            f"{chr(10).join(blocks)}\n"
        )

    def build_generation_advice_block(self, section_name, materials):
        section_materials = [material for material in materials if material["section"] == section_name]
        learned_keywords = []
        learned_headings = []

        for material in section_materials:
            learned_keywords.extend(material["keywords"])
            learned_headings.extend(material["headings"])

        default_advice = self.build_default_generation_advice(section_name)
        image_keywords = self.build_image_search_keywords(section_name, learned_keywords)
        headings_text = "、".join(self.unique_items(learned_headings)[:8]) or "暂无素材结构，先使用内置结构"
        advice_text = "\n".join([f"- {item}" for item in default_advice])
        image_text = "\n".join([f"- {keyword}" for keyword in image_keywords])

        return (
            f"## {section_name} 生成建议\n\n"
            f"- 可参考结构：{headings_text}\n"
            f"{advice_text}\n\n"
            f"## {section_name} 图片搜索建议\n\n"
            f"{image_text}\n"
        )

    def build_production_techniques_content(self, user_task, materials):
        time_text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        material_sections = self.unique_items([material["section"] for material in materials])
        all_sections = self.unique_items(["shared", "china", "word", "ppt", "excel"] + material_sections)

        blocks = []
        for section_name in all_sections:
            blocks.append(self.build_production_techniques_block(section_name, materials))
        blocks_text = "\n".join(blocks).rstrip()

        return (
            "# 通用制作技巧库\n\n"
            "这个文件由 Learning Agent 根据优秀素材自动更新。\n\n"
            f"## 原始需求\n\n{user_task}\n\n"
            f"## 更新时间\n\n{time_text}\n\n"
            "## 使用方式\n\n"
            "- Word / PPT / Excel Agent 会读取 shared、china 和自身板块技巧。\n"
            "- 新素材加入 materials 后，重新运行 Learning Agent 即可刷新技巧。\n"
            "- 技巧重点覆盖版面设计、文案生成、图片查找、图片生成和数据表达。\n\n"
            f"{blocks_text}\n"
        )

    def build_production_techniques_block(self, section_name, materials):
        section_materials = [material for material in materials if material["section"] == section_name]
        learned_headings = []
        learned_keywords = []

        for material in section_materials:
            learned_headings.extend(material["headings"])
            learned_keywords.extend(material["keywords"])

        default_techniques = self.build_default_production_techniques(section_name)
        learned_techniques = self.build_learned_production_techniques(section_name, learned_headings, learned_keywords)
        techniques = self.unique_items(default_techniques + learned_techniques)[:10]
        technique_text = "\n".join([f"- {technique}" for technique in techniques])

        return f"## {section_name} 制作技巧\n\n{technique_text}\n"

    def build_default_production_techniques(self, section_name):
        technique_map = {
            "shared": [
                "版面设计：先确定信息层级，把标题、重点、补充说明分开呈现。",
                "文案生成：先明确对象、目的和行动，再补充细节和证据。",
                "图片查找：优先找真实场景图、产品图、流程图、数据图或案例截图。",
                "图片生成：提示词要写清主体、场景、风格、比例和用途。",
            ],
            "china": [
                "中国素材：中文办公内容优先参考国内素材，表达更贴近实际使用场景。",
                "中国素材：查找国内活动视觉、营销海报、图标和模板时优先记录来源。",
            ],
            "word": [
                "Word：段落先搭结构，再润色语言，最后检查标题层级。",
                "Word：长文档要增加摘要、结论和待确认事项。",
            ],
            "ppt": [
                "PPT：每页只讲一个重点，标题要表达这一页的结论。",
                "PPT：图片和图表要服务观点，不要只做装饰。",
            ],
            "excel": [
                "Excel：先保证字段稳定和数据干净，再考虑图表和看板。",
                "Excel：图表要围绕趋势、对比、占比或异常来选择。",
            ],
        }

        return technique_map.get(section_name, ["先明确目标，再组织内容。"])

    def build_learned_production_techniques(self, section_name, learned_headings, learned_keywords):
        techniques = []
        heading_text = "、".join(self.unique_items(learned_headings)[:5])
        keyword_text = "、".join(self.unique_items(learned_keywords)[:5])

        if heading_text:
            techniques.append(f"{section_name}：可参考素材结构：{heading_text}。")

        if keyword_text:
            techniques.append(f"{section_name}：常见技巧关键词包括：{keyword_text}。")

        return techniques

    def build_default_generation_advice(self, section_name):
        advice_map = {
            "word": [
                "正文按背景、目标、重点内容、下一步计划组织。",
                "标题要短，段落要清楚，避免堆长句。",
                "图片适合放流程图、结果截图或业务场景图。",
            ],
            "excel": [
                "表头字段要稳定，数据区和备注区分开。",
                "第一行写表格类型，第二行保留原始需求，方便追溯。",
                "图片适合用作图标、看板截图或数据来源截图。",
            ],
            "ppt": [
                "每页只讲一个重点，控制在 3 到 5 条内容。",
                "先讲背景，再讲核心内容，最后给下一步计划。",
                "图片适合用真实场景图、产品界面图、流程图或数据图。",
            ],
            "research": [
                "先写调研目标，再写关键词、来源和结论记录表。",
                "资料必须记录来源和可信度。",
                "图片适合用官网截图、产品对比图或公开图表。",
            ],
            "browser": [
                "先写最短操作路径，再写异常处理。",
                "遇到登录、超时、下载失败时先记录，不继续猜测。",
                "图片适合用页面截图，并记录页面链接。",
            ],
        }

        return advice_map.get(section_name, ["先明确目标，再组织内容。", "结构清晰优先于复杂样式。"])

    def build_image_search_keywords(self, section_name, learned_keywords):
        base_keywords = {
            "word": ["办公报告 配图", "业务流程图", "项目成果 截图"],
            "excel": ["数据看板 截图", "表格模板 图标", "数据统计 图表"],
            "ppt": ["商务汇报 背景图", "项目汇报 流程图", "数据分析 可视化图"],
            "research": ["行业报告 图表", "竞品分析 截图", "产品官网 界面图"],
            "browser": ["网页截图 示例", "网站操作流程图", "浏览器页面截图"],
        }

        keywords = base_keywords.get(section_name, ["办公素材 图片", "流程图", "示例截图"])
        for keyword in self.unique_items(learned_keywords)[:3]:
            keywords.append(f"{keyword} 配图")

        return keywords[:6]

    def unique_items(self, items):
        unique_result = []
        for item in items:
            if item and item not in unique_result:
                unique_result.append(item)
        return unique_result
