from agents.excel_agent import ExcelAgent
from agents.ppt_agent import PPTAgent
from agents.qa_agent import QAAgent
from agents.research_agent import ResearchAgent
from agents.word_agent import WordAgent


class ChiefCoordinator:
    def __init__(self):
        self.word_agent = WordAgent()
        self.excel_agent = ExcelAgent()
        self.ppt_agent = PPTAgent()
        self.research_agent = ResearchAgent()
        self.qa_agent = QAAgent()

    def handle_task(self, user_task):
        if not isinstance(user_task, str):
            return "任务内容必须是文字。"

        cleaned_task = user_task.strip()
        if not cleaned_task:
            return "任务内容不能为空。"

        agent = self.choose_agent(cleaned_task)
        task_result = agent.handle(cleaned_task)
        qa_result = self.qa_agent.check_task_result(task_result, cleaned_task)

        return f"{task_result}\n\n{qa_result}"

    def choose_agent(self, user_task):
        task_text = user_task.lower()

        ppt_keywords = ["ppt", "演示", "幻灯片", "汇报", "presentation"]
        excel_keywords = ["excel", "表格", "数据", "统计", "计算", "报表", "spreadsheet"]
        word_keywords = ["word", "文档", "文章", "报告", "合同", "通知", "document"]
        research_keywords = ["调研", "搜索", "资料", "查找", "研究", "竞品", "research"]

        if self.has_keyword(task_text, research_keywords):
            return self.research_agent

        if self.has_keyword(task_text, ppt_keywords):
            return self.ppt_agent

        if self.has_keyword(task_text, excel_keywords):
            return self.excel_agent

        if self.has_keyword(task_text, word_keywords):
            return self.word_agent

        return self.word_agent

    def has_keyword(self, task_text, keywords):
        for keyword in keywords:
            if keyword in task_text:
                return True
        return False
