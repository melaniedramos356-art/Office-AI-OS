from pathlib import Path


class ProductionTechniqueLibrary:
    def __init__(self, technique_path="memory/production_techniques.md"):
        self.technique_path = Path(technique_path)

    def get_techniques(self, section_name):
        default_techniques = self.build_default_techniques(section_name)

        if not self.technique_path.exists():
            return default_techniques

        try:
            technique_content = self.technique_path.read_text(encoding="utf-8")
        except OSError:
            return default_techniques

        shared_techniques = self.extract_section_techniques(technique_content, "shared")
        china_techniques = self.extract_section_techniques(technique_content, "china")
        section_techniques = self.extract_section_techniques(technique_content, section_name)
        merged_techniques = section_techniques + shared_techniques + china_techniques

        return self.unique_texts(merged_techniques)[:8] or default_techniques

    def extract_section_techniques(self, technique_content, section_name):
        target_heading = f"## {section_name} 制作技巧"
        lines = technique_content.splitlines()
        techniques = []
        in_target_section = False

        for line in lines:
            if line.startswith("## "):
                in_target_section = line.strip() == target_heading
                continue

            if in_target_section and line.strip().startswith("- "):
                techniques.append(line.strip().replace("- ", "", 1))

        return techniques

    def build_default_techniques(self, section_name):
        shared_techniques = [
            "版面设计：先确定信息层级，把标题、重点、补充说明分开呈现。",
            "版面设计：保持对齐、留白和重复样式，避免内容挤在一起。",
            "文案生成：先明确对象、目的和行动，再补充细节和证据。",
            "文案生成：重要结论放在前面，解释和背景放在后面。",
            "图片查找：优先找真实场景图、产品图、流程图、数据图或案例截图。",
            "图片查找：记录图片来源、关键词和用途，避免后续无法追溯。",
            "图片生成：提示词要写清主体、场景、风格、比例和用途。",
            "图片生成：生成后要检查是否贴合文档主题，不能只看好不好看。",
        ]

        section_techniques = {
            "word": [
                "Word：段落先搭结构，再润色语言，最后检查标题层级。",
                "Word：长文档要增加摘要、结论和待确认事项，方便快速阅读。",
            ],
            "ppt": [
                "PPT：每页只讲一个重点，标题要表达这一页的结论。",
                "PPT：图片和图表要服务观点，不要只做装饰。",
            ],
            "excel": [
                "Excel：先保证字段稳定和数据干净，再考虑图表和看板。",
                "Excel：图表要围绕一个问题，例如趋势、对比、占比或异常。",
            ],
        }

        return self.unique_texts(section_techniques.get(section_name, []) + shared_techniques)[:8]

    def unique_texts(self, texts):
        unique_results = []
        seen_texts = set()
        for text in texts:
            if not isinstance(text, str):
                continue
            cleaned_text = " ".join(text.strip().split())
            key = cleaned_text.lower()
            if not cleaned_text or key in seen_texts:
                continue
            seen_texts.add(key)
            unique_results.append(cleaned_text)
        return unique_results
