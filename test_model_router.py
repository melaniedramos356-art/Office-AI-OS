from models.model_router import ModelRouter


class AvailableFailingClient:
    def is_available(self):
        return True

    def generate(self, task_type, prompt):
        return "DeepSeek 调用失败：模拟错误"


class AvailableSuccessClient:
    def is_available(self):
        return True

    def generate(self, task_type, prompt):
        return "{\"title\":\"可用模型结果\"}"


class UnavailableClient:
    def is_available(self):
        return False

    def generate(self, task_type, prompt):
        return "不应该调用"


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
    router = ModelRouter(use_real_models=True)
    router.provider_clients["deepseek"] = AvailableSuccessClient()
    router.provider_clients["kimi"] = UnavailableClient()
    router.provider_clients["openai"] = UnavailableClient()
    generation = router.generate("excel", "帮我规划客户数据表字段")

    if generation["route"]["provider"] != "deepseek":
        raise AssertionError("Excel 任务没有路由到模拟 DeepSeek。")

    if not generation["result"].strip():
        raise AssertionError("模拟 DeepSeek 返回为空。")

    print("测试通过：Model Router 可以处理 DeepSeek 路由，不触发真实 API")


def test_model_router_falls_back_after_provider_failure():
    router = ModelRouter(use_real_models=True)
    router.provider_clients["deepseek"] = AvailableFailingClient()
    router.provider_clients["openai"] = AvailableSuccessClient()
    router.provider_clients["kimi"] = UnavailableClient()

    generation = router.generate("excel", "帮我生成客户数据表")

    if generation["route"]["provider"] != "openai":
        raise AssertionError(f"DeepSeek 失败后没有切换到 OpenAI：{generation}")

    if len(generation.get("attempts", [])) < 2:
        raise AssertionError(f"模型尝试记录不完整：{generation}")

    print("测试通过：Model Router 会在模型失败后自动降级到下一个可用模型")


def test_model_router_can_route_to_kimi():
    router = ModelRouter(use_real_models=True)
    router.provider_clients["openai"] = UnavailableClient()
    router.provider_clients["kimi"] = AvailableSuccessClient()
    router.provider_clients["deepseek"] = UnavailableClient()

    route_info = router.route("word")
    if route_info["provider"] != "kimi":
        raise AssertionError(f"OpenAI 不可用时没有路由到 Kimi：{route_info}")

    generation = router.generate("word", "帮我写一份中文文档")
    if generation["route"]["provider"] != "kimi":
        raise AssertionError(f"生成时没有使用 Kimi：{generation}")

    print("测试通过：Model Router 可以路由到 Kimi")


def test_model_router_returns_local_after_all_real_providers_fail():
    router = ModelRouter(use_real_models=True)
    router.provider_clients["deepseek"] = AvailableFailingClient()
    router.provider_clients["openai"] = AvailableFailingClient()
    router.provider_clients["kimi"] = AvailableFailingClient()

    generation = router.generate("word", "帮我写一份文档")

    if generation["route"]["provider"] != "local":
        raise AssertionError(f"真实模型都失败后没有回到本地模型：{generation}")

    if "Mock 模型已生成占位结果" not in generation["result"]:
        raise AssertionError(f"本地兜底结果异常：{generation}")

    print("测试通过：Model Router 会在真实模型全部失败后回到本地兜底")


def main():
    run_route_test("word", ["kimi", "deepseek", "local"])
    run_route_test("excel", ["deepseek", "kimi", "local"])
    run_route_test("ppt", ["kimi", "deepseek", "local"])
    run_route_test("research", ["kimi", "deepseek", "local"])
    run_route_test("browser", ["deepseek", "kimi", "local"])
    run_route_test("qa", ["deepseek", "kimi", "local"])
    run_route_test("learning", ["deepseek", "kimi", "local"])
    run_route_test("image", ["local"])
    test_mock_generation()
    test_deepseek_route_generation()
    test_model_router_falls_back_after_provider_failure()
    test_model_router_can_route_to_kimi()
    test_model_router_returns_local_after_all_real_providers_fail()


if __name__ == "__main__":
    main()
