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
        pipeline_steps = self.build_quality_pipeline_steps(user_task)

        return (
            ["## 入口判断", f"- {entry_mode}"]
            + ["", "## 去重后的执行流程"]
            + pipeline_steps
        )

    def detect_entry_mode(self, user_task):
        if "chatgpt" in user_task.lower() or "codex" in user_task.lower() or "管家" in user_task:
            return "优先使用 ChatGPT App / Codex 管家做需求理解、任务拆解和模型分配。"

        return "没有 ChatGPT 管家时，使用 Office-AI-OS 本地核心直接执行。"

    def build_quality_pipeline_steps(self, user_task):
        steps = []

        steps.append("- Codex / ChatGPT App 先把需求压缩成：文件类型、读者、主题、交付标准。")

        if self.has_file_keyword(user_task):
            steps.append("- File Reader Agent 读取参考文件，只提取结构、版式、文案风格和数据表达。")

        if self.needs_web_inspiration(user_task):
            steps.append("- Codex 优先搜索网页优质案例并筛选技巧；本地运行时由 Web Case Agent 兜底，搜索词、网站和结果先去重。")

        steps.append("- Learning Agent 把可复用技巧写入 memory，已有技巧不重复写入。")
        steps.append(self.build_model_step(user_task))
        steps.extend(self.build_office_steps(user_task))
        steps.append("- QA Agent 检查最终文件是否完整、可打开、没有提示词或占位内容。")

        return self.unique_lines(steps)

    def build_model_step(self, user_task):
        if "图片" in user_task or "视觉" in user_task or "版面" in user_task:
            return "- Model Router 优先调用适合视觉和版面判断的模型，未接入时用本地技巧兜底。"

        if "数据" in user_task or "excel" in user_task.lower() or "表格" in user_task:
            return "- Model Router 优先调用 DeepSeek 处理数据逻辑、字段设计和检查。"

        if "文案" in user_task or "word" in user_task.lower() or "润色" in user_task:
            return "- Model Router 优先调用 OpenAI API / Kimi / DeepSeek 处理文案和长文档结构。"

        return "- Model Router 按任务类型选择 OpenAI API、DeepSeek、Kimi 或本地规则。"

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

    def needs_web_inspiration(self, user_task):
        keywords = ["优质案例", "网页", "网站", "搜索", "素材", "灵感", "版面", "图片", "制作技巧", "参考"]
        for keyword in keywords:
            if keyword in user_task:
                return True
        return False

    def unique_lines(self, lines):
        unique_result = []
        seen_lines = set()

        for line in lines:
            if not isinstance(line, str):
                continue

            cleaned_line = line.strip()
            if not cleaned_line:
                continue

            key = " ".join(cleaned_line.lower().split())
            if key in seen_lines:
                continue

            seen_lines.add(key)
            unique_result.append(cleaned_line)

        return unique_result
