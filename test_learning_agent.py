from pathlib import Path

from agents.learning_agent import LearningAgent
from coordinator import ChiefCoordinator


def test_learning_agent_directly():
    materials_folder = Path("outputs/test_materials")
    memory_folder = Path("outputs/test_memory")
    word_example_folder = materials_folder / "word" / "examples"
    word_example_folder.mkdir(parents=True, exist_ok=True)

    sample_file = word_example_folder / "sample.md"
    sample_file.write_text(
        "# 测试报告素材\n\n## 背景\n\n## 目标\n\n## 下一步计划\n",
        encoding="utf-8",
    )

    agent = LearningAgent(materials_folder=materials_folder, memory_folder=memory_folder)
    result = agent.handle("请学习素材库里的优秀素材")

    if "Learning Agent 已完成素材学习" not in result:
        raise AssertionError(f"Learning Agent 没有完成学习：{result}")

    learned_path = memory_folder / "learned_techniques.md"
    index_path = memory_folder / "material_index.md"
    advice_path = memory_folder / "generation_advice.md"

    if not learned_path.exists():
        raise AssertionError(f"技巧库文件不存在：{learned_path}")

    if not index_path.exists():
        raise AssertionError(f"素材索引文件不存在：{index_path}")

    if not advice_path.exists():
        raise AssertionError(f"生成建议文件不存在：{advice_path}")

    learned_content = learned_path.read_text(encoding="utf-8")
    if "测试报告素材" not in learned_content:
        raise AssertionError("技巧库没有记录测试素材标题。")

    advice_content = advice_path.read_text(encoding="utf-8")
    if "图片搜索建议" not in advice_content:
        raise AssertionError("生成建议没有包含图片搜索建议。")

    print("测试通过：Learning Agent 可以扫描素材并生成技巧库")


def test_coordinator_routes_learning_task():
    coordinator = ChiefCoordinator()
    result = coordinator.handle_task("请学习素材库里的优秀素材")

    if "Learning Agent 已完成素材学习" not in result:
        raise AssertionError(f"Coordinator 没有分配给 Learning Agent：{result}")

    if "QA Agent 质量检查结果：通过" not in result:
        raise AssertionError(f"Learning Agent 结果没有通过 QA：{result}")

    print("测试通过：Coordinator 可以分配素材学习任务")


def main():
    test_learning_agent_directly()
    test_coordinator_routes_learning_task()


if __name__ == "__main__":
    main()
