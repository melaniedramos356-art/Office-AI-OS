from agents.production_technique_library import ProductionTechniqueLibrary


class GenerationQualityGuide:
    def __init__(self, technique_library=None):
        self.technique_library = technique_library or ProductionTechniqueLibrary()

    def build_prompt_rules(self, section_name, limit=6):
        techniques = self.technique_library.get_techniques(section_name)
        clean_techniques = self.unique_texts(techniques)[:limit]
        if not clean_techniques:
            clean_techniques = ["先明确内容目标，再优化结构、语言和视觉层级。"]

        lines = []
        for index, technique in enumerate(clean_techniques, start=1):
            lines.append(f"{index}. {technique}")

        return "\n".join(lines)

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
