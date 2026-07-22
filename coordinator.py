from agents.ai_butler_agent import AIButlerAgent
from agents.browser_agent import BrowserAgent
from agents.excel_agent import ExcelAgent
from agents.file_improvement_agent import FileImprovementAgent
from agents.file_reader_agent import FileReaderAgent
from agents.inspiration_agent import InspirationAgent
from agents.iteration_agent import IterationAgent
from agents.learning_agent import LearningAgent
from agents.office_panel_agent import OfficePanelAgent
from agents.ppt_agent import PPTAgent
from agents.qa_agent import QAAgent
from agents.research_agent import ResearchAgent
from agents.word_agent import WordAgent


class ChiefCoordinator:
    def __init__(self):
        self.ai_butler_agent = AIButlerAgent()
        self.browser_agent = BrowserAgent()
        self.file_improvement_agent = FileImprovementAgent()
        self.file_reader_agent = FileReaderAgent()
        self.inspiration_agent = InspirationAgent()
        self.iteration_agent = IterationAgent()
        self.learning_agent = LearningAgent()
        self.office_panel_agent = OfficePanelAgent()
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

        if agent in [self.file_reader_agent, self.file_improvement_agent]:
            return f"{task_result}\n\nQA Agent 质量检查结果：跳过，文件分析类任务不检查原文件是否包含任务指令。"

        qa_result = self.qa_agent.check_task_result(task_result, cleaned_task)

        return f"{task_result}\n\n{qa_result}"

    def choose_agent(self, user_task):
        task_text = user_task.lower()

        ppt_keywords = ["ppt", "演示", "幻灯片", "汇报", "presentation"]
        excel_keywords = ["excel", "表格", "数据", "统计", "计算", "报表", "spreadsheet"]
        word_keywords = ["word", "文档", "文章", "报告", "合同", "通知", "document"]
        research_keywords = ["调研", "搜索", "资料", "查找", "研究", "竞品", "research"]
        browser_keywords = ["浏览器", "网页", "网站", "打开", "链接", "网址", "url", "browser"]
        learning_keywords = ["学习素材", "素材库", "优秀素材", "技巧库", "经验库", "learning"]
        inspiration_keywords = ["找灵感", "灵感计划", "素材灵感", "优秀作品", "参考网站", "图片查找", "素材网站"]
        office_panel_keywords = ["办公板块", "办公首页", "办公功能", "办公模块", "三大办公", "交互页面"]
        butler_keywords = ["管家", "规划", "复杂任务", "修改已有文件", "参考原文件"]
        file_improvement_keywords = ["优化文件", "改进文件", "美化文件", "润色文件", "修改建议", "版面建议"]
        file_reader_keywords = ["读取文件", "分析文件", "检查文件", ".docx", ".pptx", ".xlsx"]
        iteration_keywords = ["迭代", "优化系统", "完善程序", "简化代码", "升级技巧", "制作技巧迭代"]

        if self.has_keyword(task_text, butler_keywords):
            return self.ai_butler_agent

        if self.has_keyword(task_text, iteration_keywords):
            return self.iteration_agent

        if self.has_keyword(task_text, file_improvement_keywords):
            return self.file_improvement_agent

        if self.has_keyword(task_text, file_reader_keywords):
            return self.file_reader_agent

        if self.has_keyword(task_text, learning_keywords):
            return self.learning_agent

        if self.has_keyword(task_text, office_panel_keywords):
            return self.office_panel_agent

        if self.has_keyword(task_text, inspiration_keywords):
            return self.inspiration_agent

        if self.has_keyword(task_text, browser_keywords):
            return self.browser_agent

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
