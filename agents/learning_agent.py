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
            learned_path, index_path, material_count = self.learn_from_materials(cleaned_task)
        except OSError as error:
            return f"Learning Agent 学习素材失败：{error}"

        return (
            "Learning Agent 已完成素材学习。\n"
            f"任务内容：{cleaned_task}\n"
            f"素材数量：{material_count}\n"
            f"文件位置：{learned_path}\n"
            f"索引位置：{index_path}"
        )

    def learn_from_materials(self, user_task):
        self.materials_folder.mkdir(parents=True, exist_ok=True)
        self.memory_folder.mkdir(parents=True, exist_ok=True)

        materials = self.collect_materials()
        learned_content = self.build_learned_content(user_task, materials)
        index_content = self.build_index_content(user_task, materials)

        learned_path = self.memory_folder / "learned_techniques.md"
        index_path = self.memory_folder / "material_index.md"

        learned_path.write_text(learned_content, encoding="utf-8")
        index_path.write_text(index_content, encoding="utf-8")

        return learned_path, index_path, len(materials)

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

    def unique_items(self, items):
        unique_result = []
        for item in items:
            if item and item not in unique_result:
                unique_result.append(item)
        return unique_result
