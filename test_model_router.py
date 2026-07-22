from models.model_router import ModelRouter


def run_route_test(task_type, allowed_providers):
    router = ModelRouter()
    route_info = router.route(task_type)

    if route_info["provider"] not in allowed_providers:
        raise AssertionError(
            f"模型路由错误：{task_type} 预期 {allowed_providers}，实际 {route_info['provider']}"
        )

    print(f"测试通过：{task_type} -> {route_info['provider']}")


def test_mock_generation():
    router = ModelRouter(use_real_models=False)
    generation = router.generate("ppt", "帮我做一份项目阶段汇报 PPT")

    if generation["route"]["provider"] != "local":
        raise AssertionError("关闭真实模型后，PPT 任务没有回到本地模型。")

    if "Mock 模型已生成占位结果" not in generation["result"]:
        raise AssertionError("Mock 模型没有返回占位结果。")

    print("测试通过：Model Router 可以关闭真实模型并调用本地模型")


def test_deepseek_route_generation():
    router = ModelRouter()
    generation = router.generate("excel", "帮我规划客户数据表字段")

    if generation["route"]["provider"] not in ["deepseek", "local"]:
        raise AssertionError("Excel 任务没有路由到 DeepSeek 或本地兜底模型。")

    if not generation["result"].strip():
        raise AssertionError("DeepSeek 或回退模型返回为空。")

    print("测试通过：Model Router 可以处理 DeepSeek 路由")


def main():
    run_route_test("word", ["deepseek", "local"])
    run_route_test("excel", ["deepseek", "local"])
    run_route_test("ppt", ["deepseek", "local"])
    run_route_test("research", ["deepseek", "local"])
    run_route_test("browser", ["deepseek", "local"])
    run_route_test("qa", ["deepseek", "local"])
    run_route_test("learning", ["deepseek", "local"])
    run_route_test("image", ["local"])
    test_mock_generation()
    test_deepseek_route_generation()


if __name__ == "__main__":
    main()
