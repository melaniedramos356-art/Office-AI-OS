from agents.creation_brief_agent import CreationBriefAgent
from agents.generation_quality_guide import GenerationQualityGuide
from agents.production_technique_library import ProductionTechniqueLibrary


def main():
    test_production_technique_library_prioritizes_section_techniques()
    test_quality_guide_deduplicates_techniques()
    test_creation_brief_contains_final_quality_rules()


def test_production_technique_library_prioritizes_section_techniques():
    techniques = ProductionTechniqueLibrary().get_techniques("word")
    if not techniques or not techniques[0].startswith("Word："):
        raise AssertionError(f"Word 专属技巧未优先返回：{techniques}")


def test_quality_guide_deduplicates_techniques():
    class TestTechniqueLibrary:
        def get_techniques(self, section_name):
            return ["技巧A", "技巧A", "", "技巧B"]

    rules = GenerationQualityGuide(technique_library=TestTechniqueLibrary()).build_prompt_rules("word")
    if rules.count("技巧A") != 1 or "技巧B" not in rules:
        raise AssertionError(f"质量指南未去重：{rules}")


def test_creation_brief_contains_final_quality_rules():
    content = CreationBriefAgent().build_brief("ppt", "制作项目汇报 PPT", None, "create")
    for text in ["浏览器检索", "PPT 专项要求", "动画窗格", "不要输出提示词"]:
        if text not in content:
            raise AssertionError(f"任务单缺少质量规则：{text}")


if __name__ == "__main__":
    main()
