from pathlib import Path


class TechniqueLibrary:
    def __init__(self, advice_path="memory/generation_advice.md"):
        self.advice_path = Path(advice_path)

    def get_advice(self, section_name):
        default_advice = self.build_default_advice(section_name)

        if not self.advice_path.exists():
            return default_advice

        try:
            advice_content = self.advice_path.read_text(encoding="utf-8")
        except OSError:
            return default_advice

        section_advice = self.extract_section_advice(advice_content, section_name)
        if not section_advice:
            return default_advice

        return section_advice

    def extract_section_advice(self, advice_content, section_name):
        target_heading = f"## {section_name} 生成建议"
        lines = advice_content.splitlines()
        advice_items = []
        in_target_section = False

        for line in lines:
            if line.startswith("## "):
                in_target_section = line.strip() == target_heading
                continue

            if in_target_section and line.strip().startswith("- "):
                advice_items.append(line.strip().replace("- ", "", 1))

        return advice_items[:6]

    def build_default_advice(self, section_name):
        advice_map = {
            "word": [
                "先写清楚背景、目标、重点内容和下一步计划。",
                "段落标题要直白，避免把多个主题混在一段里。",
                "如果需要图片，优先搜索流程图、场景图或成果截图。",
            ],
            "excel": [
                "表头字段要稳定，避免一列混合多种含义。",
                "把原始需求、数据区和备注区分开。",
                "如果需要图片，优先搜索图标、流程截图或数据看板参考。",
            ],
            "ppt": [
                "先搭建标题页、背景、核心内容、风险问题、下一步计划。",
                "每页只表达一个重点，正文控制在 3 到 5 条。",
                "如果需要图片，优先搜索真实场景图、产品图、流程图或数据图。",
            ],
            "research": [
                "先明确调研问题，再列关键词和资料来源。",
                "记录来源、标题、发布时间和可信度。",
                "如果需要图片，优先搜索官网截图、产品界面图或公开图表。",
            ],
            "browser": [
                "先确认目标网址、关键词和保存位置。",
                "优先走最短路径，遇到登录或超时要记录原因。",
                "如果需要图片，优先使用页面截图并记录来源链接。",
            ],
        }

        return advice_map.get(
            section_name,
            [
                "先明确目标，再生成内容。",
                "保持结构清晰，减少无关信息。",
                "如果需要图片，先确认图片来源和使用场景。",
            ],
        )
