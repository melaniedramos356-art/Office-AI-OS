from pathlib import Path

from agents.research_agent import ResearchAgent
from coordinator import ChiefCoordinator


def test_research_agent_directly():
    test_output_folder = "outputs/test_research_plans"
    agent = ResearchAgent(output_folder=test_output_folder)
    result = agent.handle("帮我调研 AI 办公工具")

    if "Research Agent 已生成资料搜索计划" not in result:
        raise AssertionError(f"没有生成资料搜索计划：{result}")

    file_line = ""
    for line in result.splitlines():
        if line.startswith("文件位置："):
            file_line = line
            break

    if not file_line:
        raise AssertionError(f"结果中没有文件位置：{result}")

    plan_path = Path(file_line.replace("文件位置：", "", 1))
    if not plan_path.exists():
        raise AssertionError(f"文件不存在：{plan_path}")

    plan_content = plan_path.read_text(encoding="utf-8")
    if "AI 办公工具" not in plan_content:
        raise AssertionError("搜索计划没有写入原始需求。")

    print(f"测试通过：Research Agent 已生成文件 {plan_path}")


def test_coordinator_routes_research_task():
    coordinator = ChiefCoordinator()
    result = coordinator.handle_task("帮我调研 AI 办公工具")

    if "Research Agent 已生成资料搜索计划" not in result:
        raise AssertionError(f"Coordinator 没有分配给 Research Agent：{result}")

    if "QA Agent 质量检查结果：通过" not in result:
        raise AssertionError(f"Research Agent 结果没有通过 QA：{result}")

    print("测试通过：Coordinator 可以分配调研任务")


def main():
    test_research_agent_directly()
    test_coordinator_routes_research_task()


if __name__ == "__main__":
    main()
