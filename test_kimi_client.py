from models.providers.kimi_client import KimiClient


def main():
    test_kimi_client_requires_api_key()
    test_kimi_client_builds_payload()
    test_kimi_client_detects_model_fallback_condition()


def test_kimi_client_requires_api_key():
    client = KimiClient()
    client.api_key = ""
    result = client.generate("qa", "请回复：Kimi 已接入")

    if "Kimi API Key 未设置" not in result:
        raise AssertionError(f"Kimi 未配置时没有给出明确提示：{result}")

    print("测试通过：Kimi 未配置 API Key 时会给出明确提示")


def test_kimi_client_builds_payload():
    client = KimiClient(model_name="test-model")
    client.model_name = "test-model"
    payload = client.build_payload("word", "帮我写一份文档")

    if payload["model"] != "test-model":
        raise AssertionError(f"Kimi 模型名没有写入 payload：{payload}")

    if payload["messages"][0]["role"] != "system":
        raise AssertionError(f"Kimi payload 缺少 system 消息：{payload}")

    if "任务类型：word" not in payload["messages"][1]["content"]:
        raise AssertionError(f"Kimi payload 缺少任务类型：{payload}")

    print("测试通过：Kimi 客户端可以构造 Chat Completions 请求")


def test_kimi_client_detects_model_fallback_condition():
    client = KimiClient(model_name="kimi-k3")
    client.model_name = "kimi-k3"
    result = client.try_model_fallback("qa", "测试", 400, "other error")

    if result:
        raise AssertionError("非模型不存在错误不应该触发 Kimi 模型降级。")

    print("测试通过：Kimi 客户端只在模型不存在时触发降级")


if __name__ == "__main__":
    main()
