import json
import os
import urllib.error
import urllib.request

from models.model_client_base import ModelClientBase


class KimiClient(ModelClientBase):
    def __init__(self, model_name=None, timeout_seconds=30, max_tokens=1800):
        self.api_key = os.environ.get("KIMI_API_KEY") or os.environ.get("MOONSHOT_API_KEY")
        self.model_name = os.environ.get("KIMI_MODEL", model_name or "kimi-k2.6")
        self.timeout_seconds = timeout_seconds
        self.max_tokens = max_tokens
        self.api_url = os.environ.get(
            "KIMI_API_URL",
            "https://api.moonshot.cn/v1/chat/completions",
        )

    def is_available(self):
        return bool(self.api_key and self.model_name)

    def generate(self, task_type, prompt):
        if not isinstance(prompt, str) or not prompt.strip():
            return "Kimi 没有收到有效提示词。"

        if not self.api_key:
            return "Kimi API Key 未设置，请先设置 KIMI_API_KEY 或 MOONSHOT_API_KEY。"

        if not self.model_name:
            return "Kimi 模型未设置，请先设置 KIMI_MODEL。"

        payload = self.build_payload(task_type, prompt)
        request = urllib.request.Request(
            self.api_url,
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                response_data = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            error_body = error.read().decode("utf-8", errors="ignore")
            fallback_result = self.try_model_fallback(task_type, prompt, error.code, error_body)
            if fallback_result:
                return fallback_result
            return f"Kimi 调用失败：HTTP {error.code}，{error_body}"
        except urllib.error.URLError as error:
            return f"Kimi 调用失败：网络错误，{error.reason}"
        except TimeoutError:
            return "Kimi 调用失败：请求超时。"
        except json.JSONDecodeError as error:
            return f"Kimi 调用失败：返回内容不是有效 JSON，{error}"

        return self.parse_response(response_data)

    def try_model_fallback(self, task_type, prompt, error_code, error_body):
        if error_code != 404 or "Not found the model" not in error_body:
            return ""

        fallback_model = "kimi-k2.6"
        if self.model_name == fallback_model:
            return ""

        original_model = self.model_name
        self.model_name = fallback_model
        result = self.generate(task_type, prompt)
        self.model_name = original_model
        return result

    def build_payload(self, task_type, prompt):
        return {
            "model": self.model_name,
            "messages": [
                {
                    "role": "system",
                    "content": "你是 Office-AI-OS 的长文档和中文办公内容助手。输出必须完整、具体、可直接放进 Word、PPT 或 Excel 成品文件。",
                },
                {
                    "role": "user",
                    "content": f"任务类型：{task_type}\n\n用户需求：{prompt}",
                },
            ],
            "temperature": 1,
            "max_tokens": self.max_tokens,
            "stream": False,
        }

    def parse_response(self, response_data):
        try:
            return response_data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError):
            return f"Kimi 返回格式异常：{response_data}"
