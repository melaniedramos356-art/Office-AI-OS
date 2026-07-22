from pathlib import Path

from agents.inspiration_agent import InspirationAgent
from coordinator import ChiefCoordinator


def test_inspiration_agent_directly():
    test_output_folder = "outputs/test_inspiration_plans"
    agent = InspirationAgent(output_folder=test_output_folder)
    result = agent.handle("帮我找 PPT 活动汇报的优秀作品和图片素材")

    if "Inspiration Agent 已生成素材灵感计划" not in result:
        raise AssertionError(f"没有生成素材灵感计划：{result}")

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
    required_texts = ["优先查找网站", "建议搜索词", "可复用制作技巧", "站酷", "Behance"]
    for text in required_texts:
        if text not in plan_content:
            raise AssertionError(f"素材灵感计划缺少内容：{text}")

    print(f"测试通过：Inspiration Agent 已生成文件 {plan_path}")


def test_coordinator_routes_inspiration_task():
    coordinator = ChiefCoordinator()
    result = coordinator.handle_task("帮我找 PPT 优秀作品和素材网站")

    if "Inspiration Agent 已生成素材灵感计划" not in result:
        raise AssertionError(f"Coordinator 没有分配给 Inspiration Agent：{result}")

    if "QA Agent 质量检查结果：通过" not in result:
        raise AssertionError(f"Inspiration Agent 结果没有通过 QA：{result}")

    print("测试通过：Coordinator 可以分配素材灵感任务")


def main():
    test_inspiration_agent_directly()
    test_coordinator_routes_inspiration_task()


if __name__ == "__main__":
    main()
