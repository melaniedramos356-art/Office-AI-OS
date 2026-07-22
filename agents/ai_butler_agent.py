class AIButlerAgent:
    """ChatGPT App 制作模式的流程管家。"""

    def handle(self, user_task):
        if not isinstance(user_task, str) or not user_task.strip():
            return "AI Butler Agent 没有收到有效任务。"

        task = user_task.strip()
        return "\n".join(
            [
                "AI Butler Agent 已生成执行计划。",
                f"任务内容：{task}",
                "",
                "## 去重后的执行流程",
                "- Chief Coordinator 根据文件类型选择 Word、PPT、Excel 或文件改进入口。",
                "- 对应 Agent 只生成一份创作任务单，统一写明内容、视觉、检索和验收标准。",
                "- 如有参考文件，File Reader Agent 用于确认文件类型；原文件与任务单一起上传。",
                "- ChatGPT App / Codex 使用浏览器、Skills、素材库和可用模型制作最终成品。",
                "- QA Agent 在最终文件生成后检查文件可打开、内容完整和要求一致。",
            ]
        )
