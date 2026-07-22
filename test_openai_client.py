import os

from models.providers.openai_client import OpenAIClient


def main():
    if not os.environ.get("OPENAI_API_KEY"):
        print("跳过测试：OPENAI_API_KEY 未设置。")
        return

    client = OpenAIClient(timeout_seconds=60)
    result = client.generate("qa", "请只回复：OpenAI 已接入")

    if "OpenAI 调用失败" in result:
        raise AssertionError(result)

    if "OpenAI API Key 未设置" in result:
        raise AssertionError(result)

    if not result.strip():
        raise AssertionError("OpenAI 返回内容为空。")

    print("测试通过：OpenAI API 可以真实调用")
    print(result.strip()[:200])


if __name__ == "__main__":
    main()
