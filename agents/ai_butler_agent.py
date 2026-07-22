class AIButlerAgent:
    def handle(self, user_task):
        if not isinstance(user_task, str) or not user_task.strip():
            return "AI Butler Agent 没有收到有效任务。"

        cleaned_task = user_task.strip()
        plan_lines = self.build_plan_lines(cleaned_task)

        return (
            "AI Butler Agent 已生成执行计划。\n"
            f"任务内容：{cleaned_task}\n\n"
            + "\n".join(plan_lines)
        )

    def build_plan_lines(self, user_task):
        entry_mode = self.detect_entry_mode(user_task)
        file_steps = self.build_file_steps(user_task)
        knowledge_steps = self.build_knowledge_steps()
        model_steps = self.build_model_steps(user_task)
        office_steps = self.build_office_steps(user_task)

        return (
            ["## 入口判断", f"- {entry_mode}"]
            + ["", "## 文件处理"]
            + file_steps
            + ["", "## 知识库调用"]
            + knowledge_steps
            + ["", "## 模型调用"]
            + model_steps
            + ["", "## 办公 Agent 执行"]
            + office_steps
            + ["", "## 质量检查", "- 最后交给 QA Agent 检查文件是否存在、内容是否完整、是否包含原始需求。"]
        )

    def detect_entry_mode(self, user_task):
        if "chatgpt" in user_task.lower() or "codex" in user_task.lower() or "管家" in user_task:
            return "优先使用 ChatGPT / Codex 管家做需求理解和任务拆解。"

        return "没有 ChatGPT 管家时，使用 Office-AI-OS 本地核心直接执行。"

    def build_file_steps(self, user_task):
        if self.has_file_keyword(user_task):
            return [
                "- 先用文件读取 Agent 读取用户提供的 Word / PPT / Excel 原文件。",
                "- 分析当前文件的问题：结构、版面、文案、图片、数据表达。",
            ]

        return [
            "- 用户没有提供原文件时，直接按需求生成新的 Word / PPT / Excel 草稿。",
            "- 生成后保留原始需求，方便后续追溯和二次修改。",
        ]

    def build_knowledge_steps(self):
        return [
            "- 读取 memory/production_techniques.md 的通用制作技巧。",
            "- 读取 materials/shared 的跨办公优秀素材。",
            "- 读取 Word / PPT / Excel 各自素材库里的专用经验。",
            "- 需要图片或活动灵感时，读取灵感网站库和数据分析网站库。",
        ]

    def build_model_steps(self, user_task):
        steps = [
            "- Model Router 负责选择模型，不让某一个 Agent 直接绑定固定模型。",
        ]

        if "图片" in user_task or "视觉" in user_task or "版面" in user_task:
            steps.append("- 图片理解、图片生成和视觉判断优先交给 Doubao / OpenAI 多模态模型。")

        if "数据" in user_task or "excel" in user_task.lower() or "表格" in user_task:
            steps.append("- 数据分析、字段建议和逻辑检查优先交给 DeepSeek。")

        if "文案" in user_task or "word" in user_task.lower() or "润色" in user_task:
            steps.append("- 文案润色、语言丰富和长文档结构优先交给 Kimi / OpenAI。")

        if len(steps) == 1:
            steps.append("- 默认先用本地知识库兜底，再按任务类型选择 DeepSeek、Doubao、Kimi 或 OpenAI。")

        return steps

    def build_office_steps(self, user_task):
        steps = []

        if "ppt" in user_task.lower() or "幻灯片" in user_task or "汇报" in user_task:
            steps.append("- PPT Agent 负责页面结构、版式建议、图片建议和最终 PPT 输出。")

        if "excel" in user_task.lower() or "表格" in user_task or "数据" in user_task:
            steps.append("- Excel Agent 负责字段设计、数据规则、图表建议和分析表输出。")

        if "word" in user_task.lower() or "文档" in user_task or "报告" in user_task or "文案" in user_task:
            steps.append("- Word Agent 负责文档结构、文案润色、语言丰富和最终 Word 输出。")

        if not steps:
            steps.append("- Chief Coordinator 根据关键词选择 Word / PPT / Excel Agent。")

        return steps

    def has_file_keyword(self, user_task):
        file_keywords = [".docx", ".pptx", ".xlsx", "已有文件", "原文件", "修改", "参考"]
        for keyword in file_keywords:
            if keyword in user_task:
                return True
        return False
