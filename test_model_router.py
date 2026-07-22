from models.model_router import ModelRouter


def run_route_test(task_type, expected_provider):
    router = ModelRouter()
    route_info = router.route(task_type)

    if route_info["provider"] != expected_provider:
        raise AssertionError(
            f"模型路由错误：{task_type} 预期 {expected_provider}，实际 {route_info['provider']}"
        )

    print(f"测试通过：{task_type} -> {expected_provider}")


def test_mock_generation():
    router = ModelRouter()
    generation = router.generate("ppt", "帮我做一份项目阶段汇报 PPT")

    if generation["route"]["provider"] != "kimi":
        raise AssertionError("PPT 任务没有优先路由到 Kimi。")

    if "Mock 模型已生成占位结果" not in generation["result"]:
        raise AssertionError("Mock 模型没有返回占位结果。")

    print("测试通过：Model Router 可以调用 Mock 模型")


def test_deepseek_route_generation():
    router = ModelRouter()
    generation = router.generate("excel", "帮我规划客户数据表字段")

    if generation["route"]["provider"] != "deepseek":
        raise AssertionError("Excel 任务没有路由到 DeepSeek。")

    if not generation["result"].strip():
        raise AssertionError("DeepSeek 或回退模型返回为空。")

    print("测试通过：Model Router 可以处理 DeepSeek 路由")


def main():
    run_route_test("word", "kimi")
    run_route_test("excel", "deepseek")
    run_route_test("ppt", "kimi")
    run_route_test("research", "kimi")
    run_route_test("browser", "deepseek")
    run_route_test("qa", "deepseek")
    run_route_test("learning", "deepseek")
    run_route_test("image", "doubao")
    test_mock_generation()
    test_deepseek_route_generation()


if __name__ == "__main__":
    main()
