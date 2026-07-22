from agents.excel_agent import ExcelAgent
from agents.generation_quality_guide import GenerationQualityGuide
from agents.ppt_agent import PPTAgent
from agents.production_technique_library import ProductionTechniqueLibrary
from agents.word_agent import WordAgent


class CaptureModelRouter:
    def __init__(self):
        self.prompts = []

    def generate(self, task_type, prompt):
        self.prompts.append(prompt)
        return {
            "route": {"provider": "deepseek"},
            "result": "{}",
        }


def main():
    test_production_technique_library_prioritizes_section_techniques()
    test_quality_guide_deduplicates_techniques()
    test_word_prompt_uses_quality_guide()
    test_ppt_prompt_uses_quality_guide()
    test_excel_prompt_uses_quality_guide()


def test_production_technique_library_prioritizes_section_techniques():
    library = ProductionTechniqueLibrary()
    word_techniques = library.get_techniques("word")

    if not word_techniques or not word_techniques[0].startswith("Word："):
        raise AssertionError(f"Word 专属技巧没有优先返回：{word_techniques}")

    print("测试通过：Production Technique Library 会优先返回本板块技巧")


def test_quality_guide_deduplicates_techniques():
    class TestTechniqueLibrary:
        def get_techniques(self, section_name):
            return ["技巧A", "技巧A", "", "技巧B"]

    guide = GenerationQualityGuide(technique_library=TestTechniqueLibrary())
    rules = guide.build_prompt_rules("word")

    if rules.count("技巧A") != 1 or "技巧B" not in rules:
        raise AssertionError(f"质量指南没有去重：{rules}")

    print("测试通过：Generation Quality Guide 可以去重制作技巧")


def test_word_prompt_uses_quality_guide():
    router = CaptureModelRouter()
    agent = WordAgent(model_router=router)
    agent.build_document_paragraphs("帮我写一份项目总结 Word 文档")
    assert_prompt_has_quality_rules(router.prompts[-1], "Word：段落先搭结构")
    print("测试通过：Word Agent 已接入制作技巧提示")


def test_ppt_prompt_uses_quality_guide():
    router = CaptureModelRouter()
    agent = PPTAgent(model_router=router)
    agent.build_slide_data("帮我做一份项目阶段汇报 PPT")
    assert_prompt_has_quality_rules(router.prompts[-1], "PPT：每页只讲一个重点")
    print("测试通过：PPT Agent 已接入制作技巧提示")


def test_excel_prompt_uses_quality_guide():
    router = CaptureModelRouter()
    agent = ExcelAgent(model_router=router)
    agent.build_rows("帮我整理一份客户数据 Excel 表格")
    assert_prompt_has_quality_rules(router.prompts[-1], "Excel：先保证字段稳定")
    print("测试通过：Excel Agent 已接入制作技巧提示")


def assert_prompt_has_quality_rules(prompt, expected_text):
    if "制作技巧：" not in prompt:
        raise AssertionError(f"模型提示词缺少制作技巧区：{prompt}")

    if expected_text not in prompt:
        raise AssertionError(f"模型提示词没有带入预期技巧：{expected_text}")


if __name__ == "__main__":
    main()
