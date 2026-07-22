from pathlib import Path
import json


class OfficePanelAgent:
    """桌面程序的轻量配置来源。"""

    def __init__(self, output_folder="outputs/office_panels"):
        self.output_folder = Path(output_folder)

    def handle(self, user_task):
        if not isinstance(user_task, str) or not user_task.strip():
            return "办公面板配置生成失败：需求不能为空。"

        self.output_folder.mkdir(parents=True, exist_ok=True)
        panel_path = self.output_folder / "office_panel.md"
        panel_path.write_text(self.build_panel_content(user_task.strip()), encoding="utf-8")
        return f"Office Panel Agent 已生成办公面板说明。\n文件位置：{panel_path}"

    def build_panel_data(self, user_task):
        return {
            "title": "Office-AI-OS 创作任务单",
            "user_task": user_task,
            "desktop_buttons": self.build_desktop_buttons(),
        }

    def build_desktop_buttons(self):
        return [
            {
                "label": "新建 Word",
                "agent": "Word Agent",
                "input_hint": "输入主题、用途、读者与语气",
                "example_topic": "大学生暑假安全宣传教育班会文案",
                "command_template": "帮我制作 {主题} Word 文档",
            },
            {
                "label": "新建 PPT",
                "agent": "PPT Agent",
                "input_hint": "输入主题、场景、受众与页数",
                "example_topic": "上饶望仙谷景色宣传，面向年轻游客，10页",
                "command_template": "帮我制作 {主题} PPT",
            },
            {
                "label": "新建 Excel",
                "agent": "Excel Agent",
                "input_hint": "输入用途、指标、数据来源与分析目标",
                "example_topic": "销售数据分析，包含趋势、异常提醒和行动建议",
                "command_template": "帮我制作 {主题} Excel 工作簿",
            },
            {
                "label": "改进文件",
                "agent": "File Improvement Agent",
                "input_hint": "选择需改进的 Word、PPT 或 Excel 文件",
                "example_topic": "",
                "command_template": "请改进文件 {文件路径}",
            },
            {
                "label": "参考仿写",
                "agent": "Reference Imitation Agent",
                "input_hint": "选择参考文件，并在输入框说明新主题",
                "example_topic": "按参考文件风格，重做同主题内容",
                "command_template": "请参考并仿写 {主题} {文件路径}",
            },
            {
                "label": "找素材",
                "agent": "Inspiration Agent",
                "input_hint": "输入主题和文件类型，获得素材方向",
                "example_topic": "大学生安全教育 PPT",
                "command_template": "帮我找 {主题} 优秀作品和素材网站",
            },
        ]

    def build_panel_content(self, user_task):
        panel_data = self.build_panel_data(user_task)
        buttons = "\n".join(
            f"- {button['label']}：{button['input_hint']}。输出 ChatGPT App 创作任务单。"
            for button in panel_data["desktop_buttons"]
        )
        return "\n".join(
            [
                "# Office-AI-OS 办公面板",
                "",
                f"原始需求：{user_task}",
                "",
                "## 当前工作方式",
                "本地程序只生成创作任务单；最终 Word、PPT、Excel 成品由 ChatGPT App / Codex 完成网页检索、素材筛选、排版和文件制作。",
                "",
                "## 功能入口",
                buttons,
            ]
        )
