class ExcelAgent:
    def handle(self, user_task):
        if not isinstance(user_task, str) or not user_task.strip():
            return "Excel Agent 没有收到有效任务。"

        return (
            "Excel Agent 已接收任务。\n"
            f"任务内容：{user_task}\n"
            "当前 v0.2 版本先完成任务识别与分配，后续版本会处理真实表格和数据。"
        )
