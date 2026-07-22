from coordinator import ChiefCoordinator


def main():
    coordinator = ChiefCoordinator()
    cases = [
        ("帮我做一份销售周报 PPT", "PPT 演示文稿"),
        ("帮我整理一份客户数据 Excel 表格", "Excel 工作簿"),
        ("帮我写一份项目总结 Word 文档", "Word 文档"),
    ]

    for task, expected_text in cases:
        result = coordinator.handle_task(task)
        if expected_text not in result or "任务单位置：" not in result:
            raise AssertionError(f"任务分配或任务单生成失败：{result}")

    print("测试通过：协调器可为 Word、PPT、Excel 生成创作任务单")


if __name__ == "__main__":
    main()
