from models.model_client_base import ModelClientBase


class MockModelClient(ModelClientBase):
    def generate(self, task_type, prompt):
        if not isinstance(prompt, str) or not prompt.strip():
            return "Mock 模型没有收到有效提示词。"

        return (
            "Mock 模型已生成占位结果。\n"
            f"任务类型：{task_type}\n"
            f"提示词摘要：{prompt.strip()[:80]}"
        )
