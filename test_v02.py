import os

from coordinator import ChiefCoordinator

os.environ["OFFICE_AI_USE_REAL_MODEL"] = "0"


def run_test(task_text, expected_agent_name):
    coordinator = ChiefCoordinator()
    result = coordinator.handle_task(task_text)

    if expected_agent_name not in result:
        raise AssertionError(f"测试失败：预期 {expected_agent_name}，实际结果是：{result}")

    print(f"测试通过：{task_text} -> {expected_agent_name}")


def main():
    try:
        run_test("帮我做一份销售周报 PPT", "PPT Agent")
        run_test("帮我整理一份客户数据 Excel 表格", "Excel Agent")
        run_test("帮我写一份项目总结 Word 文档", "Word Agent")
        run_test("请完善办公板块", "Office Panel Agent")
        run_test("", "任务内容不能为空")
    except Exception as error:
        print(f"测试失败：{error}")
        raise


if __name__ == "__main__":
    main()
