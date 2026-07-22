import json
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
            panel_path, data_path = self.create_panel(cleaned_task)
        except OSError as error:
            return f"Office Panel Agent 创建办公板块说明失败：{error}"

        return (
            "Office Panel Agent 已生成办公板块说明。\n"
            f"任务内容：{cleaned_task}\n"
            f"文件位置：{panel_path}\n"
            f"数据位置：{data_path}"
        )

    def create_panel(self, user_task):
        self.output_folder.mkdir(parents=True, exist_ok=True)
        time_text = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        panel_path = self.output_folder / f"office_panel_{time_text}.md"
        data_path = self.output_folder / f"office_panel_{time_text}.json"
        panel_data = self.build_panel_data(user_task)

        panel_path.write_text(self.build_panel_content(panel_data), encoding="utf-8")
        data_path.write_text(json.dumps(panel_data, ensure_ascii=False, indent=2), encoding="utf-8")
        return panel_path, data_path

    def build_panel_data(self, user_task):
        return {
            "title": "办公板块",
            "user_task": user_task,
            "cards": self.build_cards(),
            "desktop_buttons": self.build_desktop_buttons(),
            "rules": [
                "首页只放高频办公入口，不堆复杂设置。",
                "每个按钮对应一条清楚的命令，方便后续接桌面交互页面。",
                "生成和修改文件都输出新文件，不覆盖原文件。",
            ],
        }

    def build_panel_content(self, panel_data):
        card_text = "\n\n".join([self.build_card_text(card) for card in panel_data["cards"]])
        button_text = "\n".join([self.build_button_text(button) for button in panel_data["desktop_buttons"]])
        rule_text = "\n".join([f"- {rule}" for rule in panel_data["rules"]])

        return (
            "# 办公板块说明\n\n"
            f"## 原始需求\n\n{panel_data['user_task']}\n\n"
            "## 功能卡片\n\n"
            f"{card_text}\n\n"
            "## 桌面 App 按钮建议\n\n"
            f"{button_text}\n\n"
            "## 简化原则\n\n"
            f"{rule_text}\n"
        )

    def build_cards(self):
        return [
            {
                "title": "Word 文档生成",
                "agent": "Word Agent",
                "type": "create",
                "command": "帮我写一份项目总结 Word 文档",
                "output": "生成 .docx 成品文档",
            },
            {
                "title": "PPT 演示生成",
                "agent": "PPT Agent",
                "type": "create",
                "command": "帮我做一份项目汇报 PPT",
                "output": "生成 .pptx 成品演示稿",
            },
            {
                "title": "Excel 表格生成",
                "agent": "Excel Agent",
                "type": "create",
                "command": "帮我整理一份客户数据 Excel 表格",
                "output": "生成 .xlsx 成品表格",
            },
            {
                "title": "已有文件改进",
                "agent": "File Improvement Agent",
                "type": "improve",
                "command": "请生成改进版 C:\\路径\\原文件.docx",
                "output": "生成新的 Word / PPT / Excel 改进版文件",
            },
            {
                "title": "素材灵感计划",
                "agent": "Inspiration Agent",
                "type": "inspiration",
                "command": "帮我找 PPT 优秀作品和素材网站",
                "output": "生成素材网站、搜索词、图片和版面建议",
            },
            {
                "title": "质量检查",
                "agent": "QA Agent",
                "type": "check",
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

    def build_desktop_buttons(self):
        return [
            {
                "label": "新建 Word",
                "agent": "Word Agent",
                "input_hint": "输入文档主题、用途和读者",
                "command_template": "帮我写一份{主题} Word 文档",
            },
            {
                "label": "新建 PPT",
                "agent": "PPT Agent",
                "input_hint": "输入汇报主题、场景和页数方向",
                "command_template": "帮我做一份{主题} PPT",
            },
            {
                "label": "新建 Excel",
                "agent": "Excel Agent",
                "input_hint": "输入表格用途、字段和数据类型",
                "command_template": "帮我整理一份{主题} Excel 表格",
            },
            {
                "label": "改进文件",
                "agent": "File Improvement Agent",
                "input_hint": "选择 .docx、.pptx 或 .xlsx 文件",
                "command_template": "请生成改进版 {文件路径}",
            },
            {
                "label": "找素材",
                "agent": "Inspiration Agent",
                "input_hint": "输入主题和文件类型",
                "command_template": "帮我找{主题}优秀作品和素材网站",
            },
            {
                "label": "查看结果",
                "agent": "QA Agent",
                "input_hint": "展示生成文件路径和质量检查结果",
                "command_template": "生成文件后自动检查",
            },
        ]

    def build_button_text(self, button):
        return (
            f"- {button['label']}：{button['input_hint']}；"
            f"调用 {button['agent']}；命令模板：{button['command_template']}"
        )
