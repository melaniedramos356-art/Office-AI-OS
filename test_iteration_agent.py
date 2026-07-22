from pathlib import Path

from agents.iteration_agent import IterationAgent
from coordinator import ChiefCoordinator


def test_iteration_agent_writes_plan():
    test_memory_folder = "outputs/test_iteration_memory"
    agent = IterationAgent(memory_folder=test_memory_folder)
    result = agent.handle("请迭代代码和制作技巧")

    if "Iteration Agent 已生成迭代计划" not in result:
        raise AssertionError(f"Iteration Agent 没有生成计划：{result}")

    log_path = Path(extract_file_path(result))
    if not log_path.exists():
        raise AssertionError(f"迭代计划文件不存在：{log_path}")

    log_content = log_path.read_text(encoding="utf-8")
    required_texts = ["代码迭代方向", "制作技巧迭代方向", "减少重复代码", "production_techniques.md"]
    for text in required_texts:
        if text not in log_content:
            raise AssertionError(f"迭代计划缺少内容：{text}")

    experience_path = Path(extract_experience_path(result))
    if not experience_path.exists():
        raise AssertionError(f"经验库文件不存在：{experience_path}")

    experience_content = experience_path.read_text(encoding="utf-8")
    required_experience_texts = [
        "程序迭代经验",
        "制作技巧与素材查找经验",
        "代码合理性",
        "优秀作品查找",
    ]
    for text in required_experience_texts:
        if text not in experience_content:
            raise AssertionError(f"经验库缺少内容：{text}")

    print("测试通过：Iteration Agent 可以生成迭代计划")


def test_coordinator_routes_iteration_task():
    coordinator = ChiefCoordinator()
    result = coordinator.handle_task("请继续迭代系统，简化代码并升级制作技巧")

    if "Iteration Agent 已生成迭代计划" not in result:
        raise AssertionError(f"Coordinator 没有分配给 Iteration Agent：{result}")

    if "QA Agent 质量检查结果：通过" not in result:
        raise AssertionError(f"Iteration Agent 结果没有通过 QA：{result}")

    print("测试通过：Coordinator 可以分配迭代任务")


def extract_file_path(task_result):
    for line in task_result.splitlines():
        if line.startswith("文件位置："):
            return line.replace("文件位置：", "", 1).strip()
    raise AssertionError(f"结果中没有文件位置：{task_result}")


def extract_experience_path(task_result):
    for line in task_result.splitlines():
        if line.startswith("经验库位置："):
            return line.replace("经验库位置：", "", 1).strip()
    raise AssertionError(f"结果中没有经验库位置：{task_result}")


def main():
    test_iteration_agent_writes_plan()
    test_coordinator_routes_iteration_task()


if __name__ == "__main__":
    main()
