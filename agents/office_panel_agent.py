from datetime import datetime
from pathlib import Path


class OfficePanelAgent:
    def __init__(self, output_folder="outputs/office_panels"):
        self.output_folder = Path(output_folder)

    def handle(self, user_task):
        if not isinstance(user_task, str) or not user_task.strip():
            return "Office Panel Agent 没有收到有效任务。"

        cleaned_task = user_task.strip()

        try:
            panel_path = self.create_panel(cleaned_task)
        except OSError as error:
            return f"Office Panel Agent 创建办公板块说明失败：{error}"

        return (
            "Office Panel Agent 已生成办公板块说明。\n"
            f"任务内容：{cleaned_task}\n"
            f"文件位置：{panel_path}"
        )

    def create_panel(self, user_task):
        self.output_folder.mkdir(parents=True, exist_ok=True)
        panel_path = self.output_folder / self.build_file_name()
        panel_path.write_text(self.build_panel_content(user_task), encoding="utf-8")
        return panel_path

    def build_file_name(self):
        time_text = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        return f"office_panel_{time_text}.md"

    def build_panel_content(self, user_task):
        card_text = "\n\n".join([self.build_card_text(card) for card in self.build_cards()])
        desktop_text = "\n".join([f"- {item}" for item in self.build_desktop_items()])

        return (
            "# 办公板块说明\n\n"
            f"## 原始需求\n\n{user_task}\n\n"
            "## 功能卡片\n\n"
            f"{card_text}\n\n"
            "## 桌面 App 按钮建议\n\n"
            f"{desktop_text}\n\n"
            "## 简化原则\n\n"
            "- 首页只放高频办公入口，不堆复杂设置。\n"
            "- 每个按钮对应一条清楚的命令，方便后续接桌面交互页面。\n"
            "- 生成和修改文件都输出新文件，不覆盖原文件。\n"
        )

    def build_cards(self):
        return [
            {
                "title": "Word 文档生成",
                "agent": "Word Agent",
                "command": "帮我写一份项目总结 Word 文档",
                "output": "生成 .docx 文档草稿",
            },
            {
                "title": "PPT 演示生成",
                "agent": "PPT Agent",
                "command": "帮我做一份项目汇报 PPT",
                "output": "生成 .pptx 演示稿草稿",
            },
            {
                "title": "Excel 表格生成",
                "agent": "Excel Agent",
                "command": "帮我整理一份客户数据 Excel 表格",
                "output": "生成 .xlsx 表格草稿",
            },
            {
                "title": "已有文件改进",
                "agent": "File Improvement Agent",
                "command": "请生成改进版 C:\\路径\\原文件.docx",
                "output": "生成新的 Word / PPT / Excel 改进版文件",
            },
            {
                "title": "素材灵感计划",
                "agent": "Inspiration Agent",
                "command": "帮我找 PPT 优秀作品和素材网站",
                "output": "生成素材网站、搜索词、图片和版面建议",
            },
            {
                "title": "质量检查",
                "agent": "QA Agent",
                "command": "生成文件后自动检查",
                "output": "检查文件是否存在、是否为空、是否包含原始需求",
            },
        ]

    def build_card_text(self, card):
        return (
            f"### {card['title']}\n\n"
            f"- 调用对象：{card['agent']}\n"
            f"- 示例命令：{card['command']}\n"
            f"- 输出结果：{card['output']}"
        )

    def build_desktop_items(self):
        return [
            "新建 Word：输入需求后调用 Word Agent。",
            "新建 PPT：输入需求后调用 PPT Agent。",
            "新建 Excel：输入需求后调用 Excel Agent。",
            "改进文件：选择本地文件后调用 File Improvement Agent。",
            "找素材：输入主题后调用 Inspiration Agent。",
            "查看结果：展示生成文件路径和 QA 检查结果。",
        ]
