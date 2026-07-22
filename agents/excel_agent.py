from agents.creation_brief_agent import CreationBriefAgent


class ExcelAgent:
    """Excel 需求入口：只生成高质量制作任务单。"""

    def __init__(self, creation_brief_agent=None):
        self.creation_brief_agent = creation_brief_agent or CreationBriefAgent()

    def handle(self, user_task):
        return self.creation_brief_agent.handle("excel", user_task)
