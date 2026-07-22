import os

from models.providers.kimi_client import KimiClient


def main():
    if not os.environ.get("KIMI_API_KEY") and not os.environ.get("MOONSHOT_API_KEY"):
        print("跳过测试：KIMI_API_KEY 和 MOONSHOT_API_KEY 都未设置。")
        return

    client = KimiClient(timeout_seconds=60)
    result = client.generate("qa", "请只回复：Kimi 已接入")

    if "Kimi 调用失败" in result:
        raise AssertionError(result)

    if "Kimi API Key 未设置" in result:
        raise AssertionError(result)

    if not result.strip():
        raise AssertionError("Kimi 返回内容为空。")

    print("测试通过：Kimi API 可以真实调用")
    print(result.strip()[:200])


if __name__ == "__main__":
    main()
