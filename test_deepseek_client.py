import os

from models.providers.deepseek_client import DeepSeekClient


def main():
    if not os.environ.get("DEEPSEEK_API_KEY"):
        print("跳过测试：DEEPSEEK_API_KEY 未设置。")
        return

    client = DeepSeekClient(timeout_seconds=60)
    result = client.generate("qa", "请只回复：DeepSeek 已接入")

    if "DeepSeek 调用失败" in result:
        raise AssertionError(result)

    if "DeepSeek API Key 未设置" in result:
        raise AssertionError(result)

    if not result.strip():
        raise AssertionError("DeepSeek 返回内容为空。")

    print("测试通过：DeepSeek API 可以真实调用")
    print(result.strip()[:200])


if __name__ == "__main__":
    main()
