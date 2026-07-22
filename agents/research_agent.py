from datetime import datetime
from pathlib import Path

from agents.inspiration_library import InspirationLibrary


class ResearchAgent:
    def __init__(self, output_folder="outputs/research_plans"):
        self.output_folder = Path(output_folder)
        self.inspiration_library = InspirationLibrary()

    def handle(self, user_task):
        if not isinstance(user_task, str) or not user_task.strip():
            return "Research Agent 没有收到有效任务。"

        cleaned_task = user_task.strip()

        try:
            plan_path = self.create_research_plan(cleaned_task)
        except OSError as error:
            return f"Research Agent 创建资料搜索计划失败：{error}"

        return (
            "Research Agent 已生成资料搜索计划。\n"
            f"任务内容：{cleaned_task}\n"
            f"文件位置：{plan_path}"
        )

    def create_research_plan(self, user_task):
        self.output_folder.mkdir(parents=True, exist_ok=True)

        file_name = self.build_file_name()
        plan_path = self.output_folder / file_name
        plan_content = self.build_plan_content(user_task)

        plan_path.write_text(plan_content, encoding="utf-8")
        return plan_path

    def build_file_name(self):
        time_text = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        return f"research_plan_{time_text}.md"

    def build_plan_content(self, user_task):
        research_type = self.detect_research_type(user_task)
        keywords = self.build_keywords(user_task, research_type)
        inspiration_keywords = self.inspiration_library.build_search_keywords(user_task)
        inspiration_table = self.inspiration_library.build_source_table(user_task)
        steps = self.build_steps(research_type)

        keyword_text = "\n".join([f"- {keyword}" for keyword in keywords])
        inspiration_keyword_text = "\n".join([f"- {keyword}" for keyword in inspiration_keywords])
        step_text = "\n".join([f"{index + 1}. {step}" for index, step in enumerate(steps)])

        return (
            "# 资料搜索计划\n\n"
            f"## 原始需求\n\n{user_task}\n\n"
            f"## 调研类型\n\n{research_type}\n\n"
            "## 建议搜索关键词\n\n"
            f"{keyword_text}\n\n"
            "## 灵感网站优先查找\n\n"
            f"{inspiration_table}\n\n"
            "## 素材/活动灵感关键词\n\n"
            f"{inspiration_keyword_text}\n\n"
            "## 搜索步骤\n\n"
            f"{step_text}\n\n"
            "## 资料记录表\n\n"
            "| 序号 | 来源 | 标题 | 关键信息 | 是否可信 | 备注 |\n"
            "| --- | --- | --- | --- | --- | --- |\n"
            "| 1 | 待填写 | 待填写 | 待填写 | 待判断 | 待填写 |\n\n"
            "## 待确认事项\n\n"
            "- 请确认是否需要联网搜索。\n"
            "- 请确认是否需要输出正式调研报告。\n"
            "- 请确认资料来源是否有指定网站或范围。\n"
        )

    def detect_research_type(self, user_task):
        if "竞品" in user_task or "竞争" in user_task:
            return "竞品调研"

        if "市场" in user_task or "行业" in user_task:
            return "市场/行业调研"

        if "用户" in user_task or "客户" in user_task:
            return "用户/客户调研"

        if "产品" in user_task or "工具" in user_task:
            return "产品/工具调研"

        return "通用资料调研"

    def build_keywords(self, user_task, research_type):
        base_keywords = [
            user_task,
            f"{user_task} 最新资料",
            f"{user_task} 案例",
        ]

        if research_type == "竞品调研":
            return base_keywords + ["竞品对比", "功能差异", "价格对比"]

        if research_type == "市场/行业调研":
            return base_keywords + ["市场规模", "行业趋势", "用户需求"]

        if research_type == "用户/客户调研":
            return base_keywords + ["用户痛点", "客户需求", "使用场景"]

        if research_type == "产品/工具调研":
            return base_keywords + ["产品功能", "工具评测", "使用教程"]

        return base_keywords + ["背景资料", "常见问题", "参考案例"]

    def build_steps(self, research_type):
        return [
            f"明确本次调研目标：{research_type}。",
            "用建议关键词搜索公开资料。",
            "记录来源、标题、关键信息和可信度。",
            "筛掉重复、过时或来源不清楚的信息。",
            "整理成结论、证据和待确认问题。",
        ]
