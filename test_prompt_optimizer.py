from models.model_router import ModelRouter
from models.prompt_optimizer import PromptOptimizer


class CapturePromptClient:
    def __init__(self):
        self.received_prompt = ""

    def is_available(self):
        return True

    def generate(self, task_type, prompt):
        self.received_prompt = prompt
        return "{\"result\":\"ok\"}"


def main():
    test_prompt_optimizer_removes_duplicate_lines()
    test_prompt_optimizer_limits_long_prompt()
    test_model_router_uses_optimized_prompt()


def test_prompt_optimizer_removes_duplicate_lines():
    optimizer = PromptOptimizer(max_chars=2000)
    prompt = "需求：生成文档\n需求：生成文档\n\n\n要求：不要占位\n要求：不要占位"
    optimized_prompt = optimizer.optimize(prompt)

    if optimized_prompt.count("需求：生成文档") != 1:
        raise AssertionError(f"重复需求没有去掉：{optimized_prompt}")

    if optimized_prompt.count("要求：不要占位") != 1:
        raise AssertionError(f"重复要求没有去掉：{optimized_prompt}")

    print("测试通过：Prompt Optimizer 可以去掉重复行")


def test_prompt_optimizer_limits_long_prompt():
    optimizer = PromptOptimizer(max_chars=1200)
    prompt = "开头需求\n" + ("中间内容\n" * 500) + "结尾约束"
    optimized_prompt = optimizer.optimize(prompt)

    if len(optimized_prompt) > 1200:
        raise AssertionError("Prompt Optimizer 没有控制最大长度。")

    if "开头需求" not in optimized_prompt or "结尾约束" not in optimized_prompt:
        raise AssertionError(f"压缩后没有保留开头或结尾：{optimized_prompt}")

    print("测试通过：Prompt Optimizer 可以压缩超长提示词")


def test_model_router_uses_optimized_prompt():
    client = CapturePromptClient()
    router = ModelRouter(use_real_models=True, prompt_optimizer=PromptOptimizer(max_chars=2000))
    router.provider_clients["deepseek"] = client
    router.provider_clients["kimi"] = client
    router.provider_clients["openai"] = client

    generation = router.generate("excel", "需求：生成表格\n需求：生成表格\n要求：输出JSON")

    if client.received_prompt.count("需求：生成表格") != 1:
        raise AssertionError(f"Model Router 没有使用优化后的提示词：{client.received_prompt}")

    prompt_info = generation.get("prompt_info", {})
    if prompt_info.get("saved_chars", 0) <= 0:
        raise AssertionError(f"Model Router 没有记录节省字符数：{generation}")

    print("测试通过：Model Router 会把压缩后的提示词传给模型")


if __name__ == "__main__":
    main()
