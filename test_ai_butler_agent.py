from agents.ai_butler_agent import AIButlerAgent
from coordinator import ChiefCoordinator


def test_ai_butler_agent_directly():
    agent = AIButlerAgent()
    result = agent.handle("请作为 ChatGPT 管家，规划如何参考原文件修改 PPT 文案和版面")

    if "AI Butler Agent 已生成执行计划" not in result:
        raise AssertionError(f"AI 管家没有生成执行计划：{result}")

    required_texts = [
        "File Reader Agent",
        "Model Router",
        "PPT Agent",
        "QA Agent",
        "去重后的执行流程",
    ]
    for text in required_texts:
        if text not in result:
            raise AssertionError(f"AI 管家计划缺少关键内容：{text}")

    plan_lines = [line.strip() for line in result.splitlines() if line.strip().startswith("-")]
    if len(plan_lines) != len(set([line.lower() for line in plan_lines])):
        raise AssertionError("AI 管家计划存在重复步骤。")

    print("测试通过：AI Butler Agent 可以生成复杂任务执行计划")


def test_coordinator_routes_butler_task():
    coordinator = ChiefCoordinator()
    result = coordinator.handle_task("请用管家模式规划一个 Word、PPT、Excel 混合修改任务")

    if "AI Butler Agent 已生成执行计划" not in result:
        raise AssertionError(f"Coordinator 没有分配给 AI Butler Agent：{result}")

    if "QA Agent 质量检查结果：跳过" not in result:
        raise AssertionError(f"AI 管家计划应该跳过文件 QA：{result}")

    print("测试通过：Coordinator 可以分配 AI 管家规划任务")


def main():
    test_ai_butler_agent_directly()
    test_coordinator_routes_butler_task()


if __name__ == "__main__":
    main()
