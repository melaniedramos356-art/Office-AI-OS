from pathlib import Path

from agents.experience_library import ExperienceLibrary
from agents.web_case_agent import WebCaseAgent
from coordinator import ChiefCoordinator


def main():
    test_parse_duckduckgo_results_and_deduplicate()
    test_web_case_agent_writes_report_without_network()
    test_coordinator_routes_web_case_task()


def test_parse_duckduckgo_results_and_deduplicate():
    html_text = """
    <a rel="nofollow" class="result__a" href="//duckduckgo.com/l/?uddg=https%3A%2F%2Fexample.com%2Fppt">PPT Design Case</a>
    <a class="result__snippet">A strong presentation layout example.</a>
    <a rel="nofollow" class="result__a" href="//duckduckgo.com/l/?uddg=https%3A%2F%2Fexample.com%2Fppt">PPT Design Case</a>
    <a class="result__snippet">Duplicated result.</a>
    <a rel="nofollow" class="result__a" href="https://example.com/word">Word Copywriting Example</a>
    <div class="result__snippet">Speech writing and copywriting example.</div>
    """
    agent = WebCaseAgent()
    cases = agent.parse_duckduckgo_results(html_text, "PPT case")

    if len(cases) != 2:
        raise AssertionError(f"网页案例解析或去重失败：{cases}")

    if cases[0]["url"] != "https://example.com/ppt":
        raise AssertionError(f"搜索跳转链接没有清洗成功：{cases[0]['url']}")

    if "PPT" not in cases[0]["technique"]:
        raise AssertionError(f"没有推断出 PPT 技巧：{cases[0]}")

    print("测试通过：Web Case Agent 可以解析并去重网页案例")


def test_web_case_agent_writes_report_without_network():
    class TestWebCaseAgent(WebCaseAgent):
        def search_cases(self, user_task, limit=8):
            return [
                {
                    "title": "PPT Design Case",
                    "url": "https://example.com/ppt",
                    "snippet": "A strong presentation layout example.",
                    "query": "ppt",
                    "technique": "PPT：提炼页面结构、标题层级、视觉节奏和图文比例。",
                },
                {
                    "title": "PPT Design Case",
                    "url": "https://example.com/ppt",
                    "snippet": "Duplicated.",
                    "query": "ppt",
                    "technique": "PPT：提炼页面结构、标题层级、视觉节奏和图文比例。",
                },
            ]

    output_folder = "outputs/test_web_cases"
    experience_library = ExperienceLibrary("outputs/test_memory/experience_library.md")
    agent = TestWebCaseAgent(output_folder=output_folder, experience_library=experience_library)
    result = agent.handle("搜索优质案例提升大学生竞选班长 PPT 排版")

    if "Web Case Agent 已完成网页优质案例搜索" not in result:
        raise AssertionError(f"网页案例报告没有生成：{result}")

    report_path = extract_file_path(result)
    if not report_path.exists():
        raise AssertionError(f"网页案例报告不存在：{report_path}")

    content = report_path.read_text(encoding="utf-8")
    if "可学习制作技巧" not in content:
        raise AssertionError("网页案例报告没有写入制作技巧。")

    print(f"测试通过：Web Case Agent 可以生成网页案例报告 {report_path}")


def test_coordinator_routes_web_case_task():
    coordinator = ChiefCoordinator()
    agent = coordinator.choose_agent("请搜索优质案例提升 PPT 排版")
    if agent.__class__.__name__ != "WebCaseAgent":
        raise AssertionError(f"Coordinator 没有分配给 WebCaseAgent：{agent.__class__.__name__}")

    print("测试通过：Coordinator 可以分配网页案例搜索任务")


def extract_file_path(task_result):
    for line in task_result.splitlines():
        if line.startswith("文件位置："):
            return Path(line.replace("文件位置：", "", 1).strip())
    raise AssertionError(f"结果中没有文件位置：{task_result}")


if __name__ == "__main__":
    main()
