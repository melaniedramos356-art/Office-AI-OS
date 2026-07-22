import json
import os
import urllib.error
import urllib.request

from models.model_client_base import ModelClientBase


class OpenAIClient(ModelClientBase):
    def __init__(self, model_name="gpt-4.1-mini", timeout_seconds=30, max_tokens=1800):
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.model_name = os.environ.get("OPENAI_MODEL", model_name)
        self.timeout_seconds = timeout_seconds
        self.max_tokens = max_tokens
        self.api_url = "https://api.openai.com/v1/chat/completions"

    def is_available(self):
        return bool(self.api_key)

    def generate(self, task_type, prompt):
        if not isinstance(prompt, str) or not prompt.strip():
            return "OpenAI 没有收到有效提示词。"

        if not self.api_key:
            return "OpenAI API Key 未设置，请先设置 OPENAI_API_KEY。"

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
            return f"OpenAI 调用失败：HTTP {error.code}，{error_body}"
        except urllib.error.URLError as error:
            return f"OpenAI 调用失败：网络错误，{error.reason}"
        except TimeoutError:
            return "OpenAI 调用失败：请求超时。"
        except json.JSONDecodeError as error:
            return f"OpenAI 调用失败：返回内容不是有效 JSON，{error}"

        return self.parse_response(response_data)

    def build_payload(self, task_type, prompt):
        return {
            "model": self.model_name,
            "messages": [
                {
                    "role": "system",
                    "content": "你是 Office-AI-OS 的办公质量总监。输出必须简洁、具体、可直接放进 Office 成品文件。",
                },
                {
                    "role": "user",
                    "content": f"任务类型：{task_type}\n\n用户需求：{prompt}",
                },
            ],
            "temperature": 0.3,
            "max_tokens": self.max_tokens,
            "stream": False,
        }

    def parse_response(self, response_data):
        try:
            return response_data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError):
            return f"OpenAI 返回格式异常：{response_data}"
